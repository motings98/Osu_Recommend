from django.shortcuts import render
import lib_data
import user_rating
from django.shortcuts import redirect

# Create your views here.


def index(request):
    return render(request,'index.html')


def CalSimilarity_Web(request):
    return render(request, 'cal.html')



def CalSimilarity_Web_Implementation(request):
    user1_url_id = request.POST["user1"]
    user2_url_id = request.POST["user2"]
    print(user1_url_id, user2_url_id)
    user1_info = lib_data.getJsonInfo(lib_data.pp_plus_api + user1_url_id)
    user2_info = lib_data.getJsonInfo(lib_data.pp_plus_api + user2_url_id)
    result = user_rating.CalUserSimilarity_Web(user1_info, user2_info)
    user1_name = user1_info["user_data"]["UserName"]
    user2_name = user2_info["user_data"]["UserName"]
    w = user1_name + " and " + user2_name + ":" + str(result) + "\n"
    f = open("feedback.txt", "a", encoding="utf-8")
    f.write(w)
    f.close()
    return render(request, "result.html", context={'data': result, "u1n": user1_name, "u2n": user2_name})


def ResultPageFeedback(request):
    feedback = request.POST["FeedbackContent"]
    str = feedback + "\n"
    print(str)
    f = open("feedback.txt","a", encoding="utf-8")
    f.write(str)
    f.close()
    return redirect("../cal")
