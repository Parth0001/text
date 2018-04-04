from slackclient import SlackClient
import threading

slack_token = "xoxp-340075011315-340177767714-340285013234-d7850a152a1baea9367b8d4615bd5f5a"
sc = SlackClient(slack_token)


def post_chat(command):
    iblt_token = "xoxp-340075011315-340177767714-341020809062-67d2da119e807b92d97f9f7c54866532"
    iblt = SlackClient(iblt_token)
    message = '"' + command + '" -> Performed'
    if(message!=""):
        iblt.api_call(
        "chat.postMessage",
        channel="CA01L2P7E",
        text=message,
        thread_ts="1522755257.000333"
        )


def get_chat(intialChatMessages):
    while(True):
        newChat = sc.api_call(
        "channels.replies",
        channel="CA01L2P7E",
        thread_ts="1522755257.000333"
        )
        newChatMessages = []
        try:
            for message in newChat['messages']:
                try:
                    if(message['user'] == 'UA057NKM0'):
                        newChatMessages.append(message['text'])
                except KeyError:
                    message['user'] = "BOT"
            if(intialChatMessages!=newChatMessages):
                for i in range(len(intialChatMessages),len(newChatMessages)):
                    print("\nCommand : " + newChatMessages[i])
                    postThread = threading.Thread(target = post_chat, args=[newChatMessages[i]])
                    postThread.start()
                    postThread.join()
                intialChatMessages = newChatMessages
        except KeyError:
            newChat['messages'] = "NODATA   "

intialChatMessages = []
intialChat = sc.api_call(
"channels.replies",
channel="CA01L2P7E",
thread_ts="1522755257.000333"
)
for message in intialChat['messages']:
    try:
        if(message['user'] == 'UA057NKM0'):
            intialChatMessages.append(message['text'])
    except KeyError:
        message['user'] = "BOT"
getThread = threading.Thread(target = get_chat, args=[intialChatMessages])
getThread.start()
getThread.join()
