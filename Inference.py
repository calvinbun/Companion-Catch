import cv2
import numpy as np
#print("CV2 and NumPy imported successfully.")
import mediapipe as mp
#print("MediaPipe imported successfully.")
import os
import tqdm
#print("OS and TQDM imported successfully.")
import torch
import torch.nn as nn
import torch.nn.functional as F
#print("Torch imported successfully.")
from datetime import datetime
#print("DateTime imported successfully.")
import tensorboard
from torch.utils.tensorboard import SummaryWriter
#print("MP Drawings imported successfully.") 
mp_pose = mp.solutions.pose
print("All imports were successfully.")

# PyTorch models inherit from torch.nn.Module
class LSTM_Model(nn.Module):
    def __init__(self):
        super(LSTM_Model, self).__init__()
        self.lstm = nn.LSTM(33 * 2, 20, 2, batch_first=True)
        self.linear = nn.LazyLinear(4)

    def forward(self, x):
        batch_size, seq_len, num_kps, num_axes = x.size()
        x = x.view(batch_size, seq_len, num_kps * num_axes)
        #print("1", x.shape)
        h0 = torch.randn(2, batch_size, 20)
        c0 = torch.randn(2, batch_size, 20)
        #print("h0:",h0.shape)
        #print("c0:",c0.shape)
        x, (hn, cn) = self.lstm(x, (h0, c0))
        #print("2", x.shape)
        x = x[..., -1]
        x = self.linear(x)
        return x






model_file_path = "model.pt"
if os.path.exists(model_file_path):
    # Check if the model architecture matches your code
    model = LSTM_Model()  # Ensure that this matches the model architecture
    try:
        model.load_state_dict(torch.load(model_file_path))
        model.eval()  # Set the model to evaluation mode
        print("Model successfully loaded.")
    except Exception as e:
        print("Error loading model:", e)
else:
    print(f"Model file '{model_file_path}' not found.")







# model = LSTM_Model()
# print("model")

# model.load_state_dict(torch.load("model.pt"))
# print("Model successfully loaded.")


cap = cv2.VideoCapture(0)
print("cap done")
act = {0 : "FALL", 1 : "SIT", 2 : "WALK"}

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
sizeframe = (frame_width, frame_height)
result = cv2.VideoWriter('VIDEOHERE.mov', cv2.VideoWriter_fourcc(*'MJPG'),10, sizeframe)


mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

drawAct = ""
pose_list = []
single_pose_list = []
with torch.no_grad():
    with mp_pose.Pose(min_detection_confidence = 0.1, min_tracking_confidence = 0.1) as pose:
        print("mp_poses.poses")
        while cap.isOpened():
            
            success, image = cap.read()
            if success:
                        
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                results = pose.process(image)

                # Draw the pose annotation on the image.
                

                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                    )





                if results.pose_landmarks:
                    keypoint = np.array([[res.x, res.y] for res in results.pose_landmarks.landmark]).flatten()
                    keypoint = np.array_split(keypoint, 33)
                    single_pose_list.append(keypoint)

                    
                
                print(len(single_pose_list))                    
                    
                    
                    
                    #mp_drawing.draw_landmarks(image,pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing_styles.get_default_pose_landmarks_style(), mp_drawing_styles.get_default_pose_connections_style())
                    
                if len(single_pose_list) >= 60:
                    pose_list_tensor = torch.tensor(single_pose_list).float()#.unsqueeze(0)
                    print(pose_list_tensor.size())
                    output = model(pose_list_tensor)
                    print(output.size())
                    prob = torch.nn.functional.softmax(output)
                    prediction = torch.argmax(prob).item()
                    single_pose_list.clear()
                    drawAct = act.get(int(prediction))
                    
                    print(drawAct)
                # image = cv2.flip(image, 1)
                #cv2.rectangle(image, (10, 10), (500, 600),(0, 255, 0), -1)
                cv2.putText(image, drawAct, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
                
                result.write(image)
                 
                
                cv2.imshow('Frame', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        cap.release()
        
        cv2.destroyAllWindows()