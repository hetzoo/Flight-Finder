from configparser import ConfigParser
from amadeus import Client, ResponseError
import google.generativeai as genai
import customtkinter
from customtkinter import *
from PIL import Image
import os

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

app = CTk()
root = customtkinter.CTk()
root.geometry("1500x500")

framel = customtkinter.CTkFrame(master=root, fg_color="#4b86b4", border_color="#2a4d69", border_width=2)
framel.pack(side="left",fill="both",expand=True)

frame2 = customtkinter.CTkFrame(master=root, fg_color="#adcbe3", border_color="#2a4d69", border_width=2)
frame2.pack(side="right",fill="both",expand=True)

frame3 = customtkinter.CTkFrame(master=root, fg_color="#63ace5", border_color="#2a4d69", border_width=2)
frame3.pack(side="bottom",fill="both",expand=True)


label=customtkinter.CTkLabel(master=framel, text="Flight Finder!", font=("Arial",50))
label.pack(expand=True,pady=12,padx=10)

label2=customtkinter.CTkLabel(master=frame3, text="Things to Do!", font=("Arial",30))
label2.pack(expand=True,pady=12,padx=10)

label3=customtkinter.CTkLabel(master=frame2, text="Flights Available", font=("Arial",30))
label3.pack(expand=True,pady=12,padx=10)

amadeus = Client(
    client_id='r4N0yHOJoArnGBGVwW313lFxjhnQGXpV',
    client_secret='6UEBpP8iJFGvEHyS'
)

entry1=customtkinter.CTkEntry(master=framel, placeholder_text="Origin Airport")
entry1.pack(pady=12,padx=10)

entry2=customtkinter.CTkEntry(master=framel, placeholder_text="Destination Airport")
entry2.pack(pady=12,padx=10)

entry3=customtkinter.CTkEntry(master=framel, placeholder_text="Date (YYYY-MM-DD)")
entry3.pack(pady=12,padx=30)

entry4=customtkinter.CTkEntry(master=framel, placeholder_text="Adults")
entry4.pack(pady=12,padx=10)

def genflights():

    response = amadeus.shopping.flight_offers_search.get(originLocationCode=entry1.get(),destinationLocationCode=entry2.get(),departureDate=entry3.get(),adults=entry4.get() )
    print(response.data)
    
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = 'AIzaSyDFu4nDjfxZDsHuH5O2RcQH8VbjwX5rvnM'
    genai.configure(api_key=api_key)
    model_gemini_pro = genai.GenerativeModel('gemini-pro')

    prompt = """
    turn this data into an organized table like this 
    |ID| Airline| Duration | Fare Option | Cabin | Total $ | Base $|:
    (ALWAYS MAKE SURE TO TRANSLATE CARRIER CODE TO AIRLINE NAME!!!, correctly space the data so it fits nicely and is not confusing) and if there is more than 10 flights then only show the lowest prices
    so that the AI doesnt crash
    """
    
    theresponse=prompt+" "+response.body
    humantalk = model_gemini_pro.generate_content("Name 20 Items in a bulletpoint format at things you can do near this airport code: "+entry2.get())
    response2 = model_gemini_pro.generate_content(theresponse)
    
    lon= model_gemini_pro.generate_content("Respond with only the longitude of This airport:"+entry2.get())
    lat= model_gemini_pro.generate_content("Respond with only the latitude of this airport:"+entry2.get())
    
    
    label2= customtkinter.CTkLabel(master=frame3, text=humantalk.text, justify=customtkinter.CENTER)
    label2.pack(pady=12,padx=10)

    label4= customtkinter.CTkLabel(master=frame2, text=response2.text, justify=customtkinter.LEFT)
    label4.pack(pady=12,padx=10)
img = Image.open("images/airplane.png")
button=customtkinter.CTkButton(master=framel, text="Find Flights!", corner_radius=32, command=genflights)
button.pack(pady=12,padx=10)



root.mainloop()
os.system("cls")

    
