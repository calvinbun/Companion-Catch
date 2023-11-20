# CompanionCatch
Fall Detection App

Go to this website: https://www.anaconda.com/download/ (Checked: Latest Version 11/19/2023)
Download anaconda from this website right at the top.

Search "Anaconda Prompt (anaconda3)" in Windwows Search Bar, then press enter to go into the prompt

Run these commands in Anaconda Prompt (anaconda3); Please Paste 1 by 1:
conda update -n base -c defaults conda
conda create -n myenv python=3.8                                          (Press y if it asks you to)
conda activate myenv
conda install pytorch torchvision torchaudio cpuonly -c pytorch           (Press y if it asks you to)
conda install opencv
pip install mediapipe
conda install pyqt                                                        (Press y if it asks you to)
conda install tqdm                                                        (Press y if it asks you to)
conda install tensorboard                                                 (Press y if it asks you to)

DON'T CLOSE THIS YET

After that, go to this website https://github.com/calvinbun/Companion-Catch
Press code, and then press download ZIP.

Go to Downloads
Right Click the ZIP file and press extract all, then press extract
Now you can delete the ZIP file

Go back to the Anaconda Prompt and paste this:
cd /../..
cd %USERPROFILE%\Downloads\Companion-Catch-main\Companion-Catch-main
python app.py
