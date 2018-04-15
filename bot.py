import praw
import random
import translate
from authentication import USERNAME, PASSWORD, USER_AGENT, CLIENT_ID, CLIENT_SECRET

# For TO-DO, look at note on phone

user_agent = USER_AGENT
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
username = USERNAME
password = PASSWORD

r = praw.Reddit(user_agent=user_agent, client_id=client_id, client_secret=client_secret,
                username=username, password=password)
r.read_only = False


def lang_roller(lang):   # Randomly chooses middle languages (ie EN > X > Y > Z > EN)
    if lang == 1:  # spanish
        chosen_lang = ["es", "Spanish"]
    elif lang == 2:  # french
        chosen_lang = ["fr", "French"]
    elif lang == 3:  # chinese (traditional)
        chosen_lang = ["zh-TW", "Chinese (Traditional)"]
    elif lang == 4:  # russian
        chosen_lang = ["ru", "Russian"]
    elif lang == 5:  # hebrew
        chosen_lang = ["iw", "Hebrew"]
    elif lang == 6:  # korean
        chosen_lang = ["ko", "Korean"]
    elif lang == 7:  # dutch
        chosen_lang = ["nl", "Dutch"]
    else:
        chosen_lang = ["es", "Spanish"]

    return chosen_lang


langList = random.sample(range(1, 8), 3)  # langList is a list of 3 numbers, non-repeating, between 1 and 7
rolled_lang1 = (lang_roller(langList[0]))
rolled_lang2 = (lang_roller(langList[1]))
rolled_lang3 = (lang_roller(langList[2]))


def trans_it(text, lang_1, lang_2, lang_3):  # Uses translate.translate function and prints everything out nicely.
    print("English > ", rolled_lang1[1], " > ", rolled_lang2[1], " > ", rolled_lang3[1], " > English")
    print("Original: ", text)
    translated_string = translate.translate(text, lang_1[0], lang_2[0], lang_3[0])
    print("SemiFluent: ", translated_string)


#teststring = "With Jeff Bezos having $116.8 billion and the average person having 100 billion brain cells, Jeff Bezos literally has more money than sense."
#trans_it(teststring, rolled_lang1, rolled_lang2, rolled_lang3)  # Function prints, doesn't return value. Tweak maybe

subreddit = r.subreddit('ShowerThoughts')
submissionList = []
for submission in subreddit.hot(limit=2): # Increase this number if you want more posts fetched
    if submission.stickied == 0: #Excludes stickied posts from printout
        submissionList.append(submission) # submissionList is now a list of (10-stickies) Submission entities

for submission in submissionList:
    post_title = submission.title
    # Add a step that re-rolls languages for every post
    trans_it(post_title, rolled_lang1, rolled_lang2, rolled_lang3)
    print('\n')
    