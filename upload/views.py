from django.shortcuts import render
from .forms import Profile_Form
from .models import User_Profile
import pandas as pd

IMAGE_FILE_TYPES = ['xlsx', 'csv']

def create_profile(request):
    form = Profile_Form()
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.display_picture = request.FILES['display_picture']
            file_type = user_pr.display_picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'profile_maker/error.html')
            user_pr.save()
            
            def splitt(x):
                li = x.split(" ")
                if len(li[2]) == 1:
                    li[2] = "0"+f"{li[2]}"
                if len(li[4]) == 1:
                    li[4] = "0"+f"{li[4]}"
                a = f"{li[0]}-{li[2]}-{li[4]}"
                return a

            def calculate_y(x):
                li = x.split("-")
                return li[0]


            def calculate_m(x):
                li = x.split("-")
                return li[1]


            def calculate_d(x):
                li = x.split("-")
                return li[2]


            df = pd.read_excel(request.FILES['display_picture'])
            df['Age2'] = df['Age'].apply(splitt)
            df['Y'] = df['Age2'].apply(calculate_y)
            df['M'] = df['Age2'].apply(calculate_m)
            df['D'] = df['Age2'].apply(calculate_d)
            df = df.sort_values(by=['Total Marks', 'Y', 'M', 'D'])
            df = df.drop(['Y', 'M', 'D', 'Age2'], axis=1)
            df = df.assign(Rank=range(len(df), 0, -1))
            df = df.sort_values(by=['Rank'])
            df.to_excel("./media/final.xlsx")

            return render(request, 'profile_maker/details.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'profile_maker/create.html', context)