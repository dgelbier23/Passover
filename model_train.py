from  ultralytics import YOLO


# # ---------------- FROM SCRATCH ---------------- #
# model = YOLO("yolov8n.yaml")    # build a new model from scratch ( can use different versions[mentioned on git])

# # Use the model
# results = model.train(data="Machine Learning\config.yaml",epochs=50)  # train the model
# # ---------------- FROM SCRATCH ---------------- #



# ----------------- FINE TUNING ---------------- #
model = YOLO('best.pt')  
results = model.train(data="Machine Learning\config.yaml",epochs=50)  # train the model 
# ----------------- FINE TUNING ---------------- #


