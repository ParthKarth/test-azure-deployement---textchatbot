#importing the libraries 
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains import ConversationChain
import pywebio
from pywebio.input import input,select
from pywebio.output import put_text, put_html, put_markdown 
import os
import re 
#from pywebio.input import *
#from pywebio.output import *

# def chatbot(template,temp1,questions=""):
#     if temp1=="cust":
#     	prompt_template = PromptTemplate(input_variables=["chat_history"], template=template)
#     elif temp1 =="agt":
#         prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
    
#     memory = ConversationBufferMemory(memory_key="chat_history")

#     llm_chain = LLMChain(
#         llm=OpenAI(openai_api_key="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",max_tokens=90),
#         prompt=prompt_template,
#         verbose=True,
#         memory=memory,
#     )

#     r=llm_chain.predict(question=questions)
#     return(r)


#@app.route("/")
def main():
    api_Key=os.getenv("api_Key")
    
    def chatbot(template,temp1,questions=""):
        if temp1=="cust":
            prompt_template = PromptTemplate(input_variables=["chat_history"], template=template)
        elif temp1 =="agt":
            prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
        
        memory = ConversationBufferMemory(memory_key="chat_history")

        llm_chain = LLMChain(
            llm=OpenAI(openai_api_key=api_Key,max_tokens=100,frequency_penalty=1,temperature=0.7,presence_penalty=1),
            prompt=prompt_template,
            verbose=True,
            memory=memory,
        )

        r=llm_chain.predict(question=questions)
        return(r)
    
    def intent(template,e1,template1,template2):
        flag=0
        count=0
        i=0
        l=[]
        t=[]

        while count>=0:
            if count ==0:
                t.append(template)
                c1= chatbot(template,"cust")
                c1= "Customer: "+c1
                reg1=re.match("^Customer:\s*(.*)",c1)[0]
                flag=1
                if flag==1:
                    #print(c1)
                    l.append(reg1)
                    #st.write(l[i])
                    put_markdown("**Customer:** \n"+l[i].replace('Customer: ', '')).style('text-align: left')
                    i+=1
                    count+=1
                    template2=template2+c1
                    flag=0
            if count%2!=0:
                if count==1: 
                    template1=template1+"\n"+c1
                    t.append(template1+e1+"\n")
                    flag=1
                    if flag==1:
                        #x=st.text_input("Your response",key=st.session_state.counter)
                        x=input("Agent Response")
                        put_markdown("**Agent Response:** \n"+x).style('text-align: right')
                        #put_text("AmplifAI LEA - A better way of responding might be:")
                        put_markdown("**AmplifAI LEA - A better way of responding might be:**").style('text-align: right').style('color: #ff5722')
                        #st.session_state.counter += 1
                        flag=0
                    if x!="":
                        #st.session_state.counter += 1
                        a1=chatbot(template1+e1+"\n","agt",x)
                        a2= "Agent: "+a1
                        l.append(a2)
                        #st.write(l[i])
                        put_text(l[i].replace('Agent: ', '')).style('text-align: right').style('text-align-last: right')
                        i+=1
                        count+=1
                        template1=template1+"\n"+a2
                        
                else:
                    template1=template1+"\n"+c2
                    t.append(template1+e1+"\n")
                    flag=1
                    if flag==1:
                        #x1=st.text_input("Your response",key=st.session_state.counter)
                        x1=input("Agent Response")
                        put_markdown("**Agent Response:** \n"+x1).style('text-align: right')
                        #put_text("AmplifAI LEA - A better way of responding might be:")
                        put_markdown("**AmplifAI LEA - A better way of responding might be:**").style('text-align: right').style('color: #ff5722')
                        flag=0
                    i+=1
                    if x1!="":
                        #st.session_state.counter += 1
                        a1=chatbot(template1+e1+"\n","agt",x1)
                        a2= "Agent: "+a1
                        l.append(a2)
                        put_text(l[i].replace('Agent: ', '')).style('text-align: right').style('text-align-last: right')
                        #st.write(l[i])
                        i+=1
                        count+=1
                        template1=template1+"\n"+a2
                    
            if count%2==0:
                if count ==2:
                    template2=template2+"\n"+a2
                    t.append(template2)
                    c2=chatbot(template2+"Customer: ","cust")
                    if c2 !="":
                        c2="Customer: "+c2
                        reg2=re.match("^Customer:\s*(.*)",c2)[0]
                        
                        #st.write(c2)
                        l.append(reg2)
                        put_markdown("**Customer:** \n"+reg2.replace('Customer: ', '')).style('text-align: left')
                        #i+=1
                        template2=template2+"\n"+c2
                        count+=1
                else :
                    template2=template2+"\n"+a2
                    t.append(template2)
                    c2=chatbot(template2+"Customer: ","cust")
                    c2="Customer: "+c2
                    reg2=re.match("^Customer:\s*(.*)",c2)[0]
                    #st.write(c2)
                    template2=template2+"\n"+c2
                    l.append(reg2)
                    #l.append(c2)
                    put_markdown("**Customer:** \n"+reg2.replace('Customer: ', '')).style('text-align: left')
                    #i+=1
                    count+=1



    y=select("Intent", options=['Billing issue', 'Military Discount', "Order Status","Product Availability","Refund Questions","Shipping or Pickup",'Issue with Order'])
    put_markdown('## AmplifAI Training Simulator').style('text-align: center')
    if y=="Billing issue":
        ## Customer 
        template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer that is having billing issues.{chat_history}
Customer:  

        """
        e1="""
        Agent: {question}
        AI:

        """

        #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
        #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        #"""+ c1+e1

        template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        """


        #cust1="Customer: "+c1
        #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

        template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer that is having billing issues.{chat_history}
        """
        intent(template=template,e1=e1,template1=template1,template2=template2)

    elif y=="Military Discount":
        template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer having queries about military discount.{chat_history}
Customer:  

        """
        e1="""
        Agent: {question}
        AI:

        """

        #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
        #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        #"""+ c1+e1

        template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
Scenario: Lets do a quick role play for a customer having queries about military discount. {chat_history}
        """


        #cust1="Customer: "+c1
        #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

        template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer having queries about military discount.{chat_history}
        """
        #template2=template2+cust1+"\n"+agent1
        intent(template=template,e1=e1,template1=template1,template2=template2)

    elif y=="Issue with Order":
        template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer having issue with his order.{chat_history}
Customer:  

        """
        e1="""
        Agent: {question}
        AI:

        """

        #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
        #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        #"""+ c1+e1

        template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
Scenario: Lets do a quick role play for a customer having issue with his order. {chat_history}
        """


        #cust1="Customer: "+c1
        #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

        template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer having issue with his order.{chat_history}
        """
        #template2=template2+cust1+"\n"+agent1
        intent(template=template,e1=e1,template1=template1,template2=template2)


    elif y=="Shipping or Pickup":
        template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer enquiring details about shipping or pickup.{chat_history}
Customer:  

        """
        e1="""
        Agent: {question}
        AI:

        """

        #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
        #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        #"""+ c1+e1

        template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
Scenario: Lets do a quick role play for a customer enquiring details about shipping or pickup. {chat_history}
        """


        #cust1="Customer: "+c1
        #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

        template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer enquiring details about shipping or pickup.{chat_history}
        """
        #template2=template2+cust1+"\n"+agent1
        intent(template=template,e1=e1,template1=template1,template2=template2)
    
    elif y=="Order Status":
        template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer enquiring the status of their order.{chat_history}
Customer:  

        """
        e1="""
        Agent: {question}
        AI:

        """

        #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
        #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        #"""+ c1+e1

        template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
Scenario: Lets do a quick role play for a customer enquiring the status of their order. {chat_history}
        """


        #cust1="Customer: "+c1
        #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

        template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer enquiring the status of their order.{chat_history}
        """
        #template2=template2+cust1+"\n"+agent1
        intent(template=template,e1=e1,template1=template1,template2=template2)

    elif y=="Product Availability":
        template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer enquiring about availability of the product.{chat_history}
Customer:  

        """
        e1="""
        Agent: {question}
        AI:

        """

        #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
        #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        #"""+ c1+e1

        template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
Scenario: Lets do a quick role play for a customer enquiring about availability of the product. {chat_history}
        """


        #cust1="Customer: "+c1
        #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

        template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer enquiring about availability of the product.{chat_history}
        """
        #template2=template2+cust1+"\n"+agent1
        intent(template=template,e1=e1,template1=template1,template2=template2)

    elif y=="Refund Questions":
        template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer who has enquiries about refund.{chat_history} \nCustomer:  

        """
        e1="""
        Agent: {question}
        AI:

        """

        #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
        #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
        #"""+ c1+e1

        template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response. 
Scenario: Lets do a quick role play for a customer who has enquiries about refund. {chat_history}
        """


        #cust1="Customer: "+c1
        #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

        template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
Scenario: Lets do a quick role play for a customer who has enquiries about refund.{chat_history}
        """
        #template2=template2+cust1+"\n"+agent1
        intent(template=template,e1=e1,template1=template1,template2=template2)




if __name__ == "__main__":
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(main, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(main, port=args.port, websocket_ping_interval=30)

