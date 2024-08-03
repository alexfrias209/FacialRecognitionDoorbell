import torch
from PIL import Image
import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
from collections import defaultdict
from ..models import MultipleImage, Account, PhoneNumber, UserProfileImage,VideoSession
from twilio.rest import Client
from django.core.files import File
from tempfile import NamedTemporaryFile
import os
import shutil
from django.core.files.base import ContentFile


def save_frame_to_user_profile(frame, user_profile, video_session):
    temp_dir = "C:/Users/alexf/OneDrive/Desktop/temp"
    with NamedTemporaryFile(suffix='.jpg', dir=temp_dir, delete=False) as temp_img:
        img_name = f"{user_profile.user.username}_frame.jpg"
        cv2.imwrite(temp_img.name, frame)

def sending(name, user_profile):
    account_sid = 'temp'
    auth_token = 'temp'
    client = Client(account_sid, auth_token)

    def sendText(mes, numbers):
        for num in numbers:
            message = client.messages \
                .create(
                    body=mes,
                    from_='+num',
                    to= num
                )
            message

    phone_numbers = PhoneNumber.objects.filter(user_profile=user_profile)
    numbers = [phone_number.phone_number.as_e164 for phone_number in phone_numbers]

    message = f"{name} is at the door"
    # sendText(message, numbers)
    print(message)
    print(numbers)

def create_embeddings(user_profile, data_path):
    mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    name_list = []
    embedding_list = []

    accounts = user_profile.account_set.all()

    for account in accounts:
        for multiple_image in account.multipleimage_set.all():
            img_path = multiple_image.images.path
            img = Image.open(img_path).convert('RGB')  
            face, prob = mtcnn(img, return_prob=True)
            if face is not None and prob > 0.90:
                emb = resnet(face.unsqueeze(0))
                embedding_list.append(emb.detach())
                name_list.append(multiple_image.account.username)

    if os.path.exists(data_path):
        saved_data = torch.load(data_path)
        saved_embedding_list = saved_data[0]
        saved_name_list = saved_data[1]

        active_names = [account.username for account in accounts]
        filtered_embeddings = []
        filtered_names = []

        for idx, name in enumerate(saved_name_list):
            if name in active_names:
                filtered_embeddings.append(saved_embedding_list[idx])
                filtered_names.append(name)

        embedding_list.extend(filtered_embeddings)
        name_list.extend(filtered_names)

    data = [embedding_list, name_list]
    torch.save(data, data_path)

    with open(data_path, 'rb') as f:
        file_name = os.path.basename(data_path)
        content = f.read()
        user_profile.data_file.save(file_name, ContentFile(content))

    return data


def facial(user_profile,video_path, video_session):
    if user_profile.data_file:
        print("TESTING1")
        with open(user_profile.data_file.path, 'rb') as f:
            saved_data = torch.load(f)
            embedding_list = saved_data[0]
            name_list = saved_data[1]
            data = [embedding_list, name_list] 
    else:
        print("TESTING2")
        data_path = 'C:/Users/alexf/OneDrive/Desktop/CSE155PROJECT1/data.pt'
        data = create_embeddings(user_profile, data_path)
    mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    print("test3")
    def face_match(frame, data, threshold=0.8):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert('RGB') 
        face, prob = mtcnn(img, return_prob=True)

        if face is None or prob < 0.90:
            return None, None

        emb = resnet(face.unsqueeze(0)).detach()

        embedding_list = data[0]
        name_list = data[1]
        dist_list = []

        for idx, emb_db in enumerate(embedding_list):
            dist = torch.dist(emb, emb_db).item()
            dist_list.append(dist)

        idx_min = dist_list.index(min(dist_list))

        if min(dist_list) > threshold:
            return "unknown", min(dist_list)

        return name_list[idx_min], min(dist_list)

    def process_video_face_recognition(video_path, data, threshold=0.8, exit_count=4, video_session=None):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
        else:
            print(f"Video file {video_path} loaded successfully")


        recognition_counts = defaultdict(int)
        recognized = False

        count = 0  

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            name, dist = face_match(frame, data, threshold)
            if name is not None and dist is not None:
                
                if count > 20:
                    break
                print(f"Face matched with: {name} With distance: {dist}")
                cv2.putText(frame, f"{name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                if name == "unknown":
                    count += 1
                    save_frame_to_user_profile(frame, user_profile, video_session)


                if name != "unknown":
                    recognition_counts[name] += 1

                if recognition_counts[name] >= exit_count:
                    print(f"{name} recognized {exit_count} times. Exiting.")
                    sending(name, user_profile)
                    recognized = True
                    break

            cv2.imshow('Video Face Recognition', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        temp_dir = "C:/Users/alexf/OneDrive/Desktop/temp"
        if (recognized == False):
            sending("Unknown", user_profile)
            for filename in os.listdir(temp_dir):
                if filename.endswith(".jpg"):
                    img_path = os.path.join(temp_dir, filename)
                    img_name = os.path.basename(img_path)
                    with open(img_path, 'rb') as img_file:
                        user_profile_image = UserProfileImage(user_profile=user_profile, video_session=video_session)
                        user_profile_image.images.save(img_name, File(img_file))
                        user_profile_image.save()
        
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


        cap.release()
        cv2.destroyAllWindows()
        

    process_video_face_recognition(video_path, data, video_session=video_session)
