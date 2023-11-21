# CompanionCatch
Fall Detection App

Go to this website: https://www.anaconda.com/download/ (Checked: Latest Version 11/19/2023)<br>
Download anaconda from this website right at the top.

Search "Anaconda Prompt (anaconda3)" in Windwows Search Bar, then press enter to go into the prompt

Run these commands in Anaconda Prompt (anaconda3); Please Paste 1 by 1:<br>
conda update -n base -c defaults conda<br>
conda create -n myenv python=3.9                                          (Press y if it asks you to)<br>
conda activate myenv<br>
conda install pytorch torchvision torchaudio cpuonly -c pytorch           (Press y if it asks you to)<br>
conda install opencv<br>
conda install -c conda-forge wxpython <br>
pip install mediapipe<br>
conda install pyqt                                                        (Press y if it asks you to)<br>
conda install tqdm                                                        (Press y if it asks you to)<br>
conda install tensorboard                                                 (Press y if it asks you to)<br>

DON'T CLOSE THIS YET

After that, go to this website https://github.com/calvinbun/Companion-Catch
Press code, and then press download ZIP.

Go to Downloads
Right Click the ZIP file and press extract all, then press extract
Now you can delete the ZIP file

Go back to the Anaconda Prompt and paste this:<br>
cd /../..<br>
cd %USERPROFILE%\Downloads\Companion-Catch-main\Companion-Catch-main<br>
python app.py
