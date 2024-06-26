import tempfile

from bag_counter import BagCounter
import cv2
import streamlit as st
from ultralytics import YOLO


@st.cache_resource
def get_model() -> YOLO:
    return YOLO("../best.pt")


FPS = 5
THRESHOLD_P1 = [0, 100]
THRESHOLD_P2 = [600, 360]

st.title("Conveyor Bag Counter")

video = st.file_uploader("Video Uploader")

model = get_model()

if video is not None:
    counter = BagCounter(THRESHOLD_P1, THRESHOLD_P2)
    with tempfile.NamedTemporaryFile("wb") as f:
        f.write(video.getbuffer())
        cap = cv2.VideoCapture(f.name)
        total_seconds = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) // FPS)

        pbar = st.progress(0, text=f"Count: {counter.count}")

        for frame_id in range(total_seconds):
            pbar.progress(frame_id / total_seconds, text=f"Count: {counter.count}")
            cap.set(cv2.CAP_PROP_POS_FRAMES, FPS * frame_id)
            _, frame = cap.read()
            out = model.track(frame, persist=True, verbose=False)[0]
            if out.boxes.id is not None:
                counter.update(out)
        pbar.empty()
        st.balloons()
        st.header("")
        message = f"{counter.count} bag{'s' if counter.count != 1 else ''}"
        st.markdown(f"<h1 style='text-align: center;'>{message}</h1>", unsafe_allow_html=True)
