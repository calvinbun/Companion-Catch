# CompanionCatch
Fall Detection App <br>
<br>
Go to this website: https://www.anaconda.com/download/ (Checked: Latest Version 11/19/2023)<br>
Download anaconda from this website right at the top. <br>
<br>
Search "Anaconda Prompt (anaconda3)" in Windows Search Bar, then press enter to go into the prompt
<br>
Run these commands in Anaconda Prompt (anaconda3); Please Paste 1 by 1:<br>
FOR THESE COMMANDS IT MAY ASK YOU TO PRESS "Yes"; type "y" and enter. <br>
conda update -n base -c defaults conda <br>
conda create -n myenv python=3.9 <br>
conda activate myenv <br>
conda install pytorch torchvision torchaudio cpuonly -c pytorch <br>
conda install opencv <br>
conda install -c conda-forge wxpython <br>
pip install mediapipe<br>
conda install pyqt <br>
conda install tqdm <br>
conda install tensorboard <br>
<br>
DON'T CLOSE THIS YET <br>
<br>
After that, go to this website https://github.com/calvinbun/Companion-Catch <br>
Press code, and then press download ZIP.<br>
<br>
Go to Downloads<br>
Right Click the ZIP file and press extract all, then press extract<br>
Now you can delete the ZIP file<br>
<br>
Go back to the Anaconda Prompt and paste this:<br>
cd /../..<br>
cd %USERPROFILE%\Downloads\Companion-Catch-main\Companion-Catch-main<br>
python app.py
