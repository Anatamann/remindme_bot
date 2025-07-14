import discord
from discord.ext import commands, tasks
import datetime as dt
import pytz
import logging
import sqlite3
import re
import spacy
from remindme_bot import database
db = database

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

ist = pytz.timezone('Asia/Kolkata') # converting the UTC time to IST

today =  dt.datetime.now(ist) # today's date in datetime format

epoc = dt.datetime.fromtimestamp(0, tz=ist)
#--------------Logging function------------------#

logging.basicConfig(
    filename='remindme_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#------------------------Bot-Events---------------#
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    rm_check_nlp.start()

@bot.event
async def on_message(message):

    ctx = await bot.get_context(message)

    if message.author == bot.user:
        return
    else:
        if bot.user.mentioned_in(message):
        # print("message content: ", message.content)
            user_msg = message.content
            mesg = user_msg.split('>')
            # print("split message:", org_msg)
            org_msg = mesg[1].strip()
            coms_msg = re.search(r'\bcoms\b',str(org_msg), re.IGNORECASE)
            # print(f"coms_msg: {coms_msg}")
            match_rm = re.search(r'\bremind(\s*:?me)?\b', str(org_msg), re.IGNORECASE)
            digit_match = re.findall(r'\d+', str(org_msg))
            # print(f"match_rm, digit_match: {match_rm}:{digit_match}")
            if match_rm and digit_match:
                val = await remindme(org_msg, ctx)
                await ctx.channel.send(f"{val}")
            elif coms_msg:
                reply = f'''
                Time notation supported:
                \n`s` or `sec` or `second` or `seconds`\n`m` or `min` or `minute` or `minutes`\n`h` or `hr` or `hrs` or `hour` or `hours`
                \n`am` or `pm`  : Using 12hour format style.
                \nEx: `@remindme_bot` remind me to call in 5min\n      `@remindme_bot` remind me to push code at 2pm'''
                await ctx.channel.send(reply)
            else:
                await ctx.channel.send('''
                    f"Yooo whats up!\n check `coms` or use the command like this:
                    \nEx: `@remindme_bot` remind me to check the code in 30min.")
                    \nThe smallest input unit is `seconds` but will advice to use `minutes` for better accuracy.
                ''')
        else:
            pass

#---------------------Functoins-------------------------------#

async def remindme(msg, ctx):
    try:
        task, time = await nlp_task(msg)
    except Exception as e:
        return e
    try:
        time_target, rm_at = await time_op(time)
    except Exception as e:
        return e
    user = await bot.fetch_user(ctx.author.id)
    if not user:
        print("somehow user not showing up in discord's database!!")
    today = dt.datetime.now(ist)
    created_at = today
    rm_at = rm_at.strftime("%Y-%m-%d %H:%M:%S.%f")
    if task and time:
        value = db.remind_in(str(task), float(time_target), str(ctx.author.id), str(created_at), str(rm_at))
        if not value:
            return (f"I got you, I will remind you about `{task}`")
        else:
            return value
    

async def nlp_task(msg):
    nlp = spacy.load("en_core_web_sm")
    sentence = msg
    doc = nlp(sentence)
    task = None
    for token in doc:
        if token.text.lower() == "to":
            print(f"inside to-block: {token.text}")
            # The verb is the head of the "to" token
            verb = token.head
            if verb.pos_ == "VERB":
                # Start building the task with the verb's base form
                task_parts = [verb.lemma_]
                # Append the rest of the verb's phrase (objects, etc.)
                for child in verb.children:
                    if child.dep_ in ("dobj", "pobj", "attr"):
                        task_parts.append(" ".join(t.text for t in child.subtree))
                task = " ".join(task_parts)
                print(f"task inside the to-block : {task}")
                break  # Exit after finding the main task

    # --- Fallback Strategy: Use noun chunks if no verb was found ---
    if not task:
        time_entities = [ent.text for ent in doc.ents if ent.label_ in ("TIME", "DATE")]
        noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text not in time_entities]

        # Exclude "me" if other, more descriptive chunks are available
        filtered_chunks = [chunk for chunk in noun_chunks if chunk.lower() != "me"]
        if filtered_chunks:
            noun_chunks = filtered_chunks
            print("inside filtered_noun_chunck-block")
        if "about" in sentence:
            try:
                about_index = sentence.lower().index("about") + len("about")
                for chunk in noun_chunks:
                    if sentence.lower().index(chunk.lower()) > about_index:
                        task = chunk
                    print(f"inside filtered_noun_chunck-block: {task}")
                    break
            except ValueError:
                pass # "about" not found or part of another word
    
    if not task and noun_chunks:
        task = max(noun_chunks, key=len)
        print(f"inside max_length block : {task}")
    # Final fallback if no task is identified
    if not task:
        task = "your task"
        print(f"final fall-block block: {task}")
    # Extract time entities separately
    time_entities = [ent.text for ent in doc.ents if ent.label_ in ("TIME", "DATE")]
    
    print("Task:", task)
    print("Time:", time_entities)
    
    if not time_entities:
        am_present = re.search(r'\b\d+(\s)?(am)$\b', sentence, re.IGNORECASE )
        pm_present = re.search(r'\b\d+(\s)?(pm)$\b', sentence, re.IGNORECASE )
        
        if am_present or pm_present:
            timer = re.findall(r'(1[0-2]|0?[1-9])(:[0-5][0-9])?', sentence)
            print(timer)
            hour, minute = timer[0]
            minute = minute.replace(":","")
            minute = minute if minute else '00'
            time_str = f"{hour}:{minute}"
            print(time_str,"\n",am_present, "\n", pm_present)
            if time_str:
                if am_present:
                    print("am is present")
                    timer = str(time_str+'am')
                elif pm_present:
                    print("pm is present")
                    timer = str(time_str+'pm')
                else:
                    pass
            else:
                pass
        else:
            time_hr = re.search(r'\b(\d+)\s*(h|hrs|hr|hours|hour)$\b',str(sentence) ,re.IGNORECASE)
            time_min = re.search(r'\b(\d+)\s*(m|min|minutes|minute)$\b',str(sentence) ,re.IGNORECASE)
            time_sec = re.search(r'\b(\d+)\s*(s|sec|second|seconds)$\b',str(sentence),re.IGNORECASE)
            time_digit = re.findall(r'\d+', str(sentence))
            time_digit = time_digit[0]
            if time_hr:
                print(f"time_hr: {time_hr}")
                timer = str( time_digit + 'hrs' )
            elif time_min:
                print(f"time_min: {time_min}")
                timer = str(time_digit + 'min')
            elif time_sec:
                print(f"time_sec: {time_sec}")
                timer = str(time_digit + 'sec')
            else:
                print(f"time_digit: {time_digit}")
                timer = str(time_digit)
    else:
        timer = str(time_entities[0])
        print(timer)

    return task, timer

async def time_op(time):
    time = str(time)
    print("time at time_op()",time)
    dtime = re.search(r'\s*(am|pm)\s*$',str(time) ,re.IGNORECASE)
    today = dt.datetime.now(ist)
    if dtime:
        print(dtime.group(1))
        entrydate = str(time).replace(" ", "")
        time_dt = dt.datetime.strptime(entrydate, "%I:%M%p")
        
        time_dt = time_dt.replace(year=today.year, month=today.month, day=today.day)

        timedt = time_dt - today
        time_target = float(timedt.seconds / 60)
        rm_at = today + dt.timedelta(minutes=float(time_target))
        return round(time_target,3), rm_at
    else:
        time_digit = re.findall(r'\d+',str(time))
        time_digit = time_digit[0]
        time_hr = re.search(r'\b(\d+)\s*(h|hr|hrs|hour|hours)$\b',str(time) ,re.IGNORECASE)
        print(f"timer_hr: {time_hr}")
        time_min = re.search(r'\b(\d+)\s*(m|min|minute|minutes)$\b',str(time) ,re.IGNORECASE)
        print(f"timer_min: {time_min}")
        time_sec = re.search(r'\b(\d+)\s*(s|sec|second|seconds)$\b',str(time),re.IGNORECASE)
        print(f"time in seconds: {time_sec}")
        if time_hr:
            time_target = int(time_digit) * 60.0
        elif time_min:
            time_target = int(time_digit) * 1.0
        elif time_sec:
            time_target = int(time_digit) * (1.0/60)
        else:        
            time_target = int(time_digit) * 1.0
            print(f"timer_only: {time_digit}")

        rm_at = today + dt.timedelta(minutes=(float(time_target)))
        return round(time_target,3), rm_at


def task_date_fn(today, id=1):
    with sqlite3.connect('remindme_bot.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
                    SELECT task_date FROM rm_check_table
                    WHERE id=?
                    ''',(int(id),))
        task_date = cursor.fetchone()
        today_f = today.strftime("%Y-%m-%d %H:%M:%S")
        if not task_date:
            print(f'added first check_date {today_f}')
            conn.execute ('''
                    INSERT INTO rm_check_table(task_date)
                    VALUES (?)
                ''',(str(today_f),))
            conn.commit()
            return today
        else:
            task_date = task_date[0]
            task_date = ist.localize(dt.datetime.strptime(task_date, "%Y-%m-%d %H:%M:%S"))
            db.rm_check_table_up(today_f, id)
            print(f'todays {id} task_check date {task_date.strftime("%Y-%m-%d %H:%M:%S")}')
            return task_date


@tasks.loop(seconds=30)
async def rm_check_nlp():
    await bot.wait_until_ready()
    today = dt.datetime.now(ist)
    check_id = 1
    task_date_check = task_date_fn(today, check_id)
    if task_date_check:    
        task_check_gaping_min = (today - task_date_check).total_seconds()
    else:
        print("First date_time_check registered on the database!!")
        return
    
    if task_check_gaping_min <= 0:
        print(f"check already done for {task_date_check}")
    else:
        task_date = today.strftime("%Y-%m-%d %H:%M:%S")
        db.rm_check_table_up(task_date, check_id)
        rm_ids = db.remind_check()
        if not rm_ids:
            print(" Empty list on reminder task ids for check!!")
        else:
            for rm_id in rm_ids:
                task_id = rm_id['rm_id']
                user_id = rm_id['user_id']
                remind_at = rm_id['remind_at']
                task = rm_id['task']
                
                time_check = ist.localize(dt.datetime.strptime(remind_at, "%Y-%m-%d %H:%M:%S.%f"))
                today = dt.datetime.now(ist)
                reminder_time_gap = (time_check - today).total_seconds()
                print("checks for reminder to user", time_check, today)
                if reminder_time_gap <= 0:
                    print("checks for reminder to user inside if block", time_check, today, reminder_time_gap)
                    try:
                        user = await bot.fetch_user(user_id)
                        result = db.remind_update(task_id)
                        if not result:
                            await user.send(f"Hey you!! you asked me to remind you about `{task}`")
                            print(f"Sent the remind to {user_id} for task: {task}")
                        else:
                            print(f"Error storing the reminder update for the {task_id} at {today}")
                    except Exception:
                        print("User not found, is he AFK?")
                else:
                    continue
    return
