# activate anaconda
cd /media/F/moveai/codes/motion_extraction/calibration/cam_intrinsics
source ~/anaconda3/etc/profile.d/conda.sh
conda activate mocap
python ./calc_intrinsics_app.py --video_dir "$1" --out_dir "$2" --viz_dir "$3"
