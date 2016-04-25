import os
import glob
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from slackbot.bot import Bot
from slackbot.bot import respond_to

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret_472191694539-lc2ajaqlc62jqlkon1se16i5fhb5maef.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
#myRepos = '/myRepos/TestBot'

#get_credentials
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    prease CLIENT_SECRET_FILE is puts same directory with botrun.py
    """
#    home_dir = os.environ.get('UserProfile')
    
#    credential_dir = os.path.join(home_dir, myRepos)
#    credential_dir = os.path.curdir()
#    if not os.path.exists(credential_dir):
#        os.makedirs(credential_dir)
#    credential_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)

#    store = oauth2client.file.Storage(credential_path)
    store = oauth2client.file.Storage(CLIENT_SECRET_FILE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#description
@respond_to('こんにちは|スラえもーん')
def response(message): 
    message.reply('ボクスラえもん！【確定】start yyyy-mm-dd hh:mm end yyyy-mm-dd hh:mmの書式で書いてね!')
    print(os.path.curdir)

#joke
@respond_to('出して|だして|出せ|だせ|^おい$')
def response(message): 
    message.reply(glob.glob(os.path.curdir + "/*"))
    message.reply('うるせーー')

@respond_to('どこでもドア')
def response(message): 
    message.reply('故障中')

@respond_to('タケコプター')
def response(message): 
    message.reply('どっか落っことした')

@respond_to('スモールライト')
def response(message): 
    message.reply('ねえよんなもん')

@respond_to('ビッグライト')
def response(message): 
    message.reply('ないない')

#main
@respond_to('【確定】.*start.*end.*')
def yoyaku(message):
    import json
    import re

    #oauth2認証
#    oCred = get_credentials()
#    oHttp = oCred.authorize(httplib2.Http())

    #カレンダーサービスオブジェクトの取得
#    oService = discovery.build('calendar', 'v3', http=oHttp)

    #チャットメッセージの取得
    jsMsgBody = json.dumps(message.body)

    #jsonデータの定義
    strSummary = '自動化TF_MTG'  #summary
    strLocation = ''    #location
    strTimeZone = 'Asia/Tokyo'    #start.timeZone

    #日付の整形
    p=re.compile('start\s*(\d{4}[/|-|年]\d{1,2}[/|-|月]\d{1,2}日*)\s*(\d{1,2}[:|時]\d{1,2})')
    m=p.search(jsMsgBody).group
    p=re.compile('(/|(年|月|日))')
    dStart = p.sub('-', m(1)) + 'T' + m(2) + ':00+09:00'  #start.dateTime

    p=re.compile('end\s*(\d{4}[/|-|年]\d{1,2}[/|-|月]\d{1,2}日*)\s*(\d{1,2}[:|時]\d{1,2})')
    m=p.search(jsMsgBody).group
    p=re.compile('(/|(年|月|日))')
    dEnd = p.sub('-', m(1)) + 'T' + m(2) + ':00+09:00' #end.dateTime

    #events.jsonの生成
    event = {
        'summary':strSummary,
        'location':strLocation,
        'start':{
            'dateTime':dStart,
            'timeZone':strTimeZone
            },
        'end':{
            'dateTime':dEnd,
            'timeZone':strTimeZone
            }
        }

    #イベントの登録
#    event = oService.events().insert(calendarId='primary', body=event).execute()
#    message.reply("ほれ %s" % (event.get('htmlLink')))

def main():

    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
