"use client";
import Image from "next/image";
import { useState } from "react";
<<<<<<< HEAD

export default function Home() {

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]); // Add user message
    setInput("");
    setLoading(true);

    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: input }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let botMessage = { role: "assistant", content: "" }; // AI message starts empty
    setMessages((prev) => [...prev, botMessage]); // Add empty AI message to array

    const readStream = async () => {
      const { value, done } = await reader.read();
      if (done) {
        setLoading(false);
        return;
      }

      let token = decoder.decode(value);

      setMessages((prev) => {
        let updatedMessages = [...prev];
        updatedMessages[updatedMessages.length - 1] = {
          role: "assistant",
          content: updatedMessages[updatedMessages.length - 1].content + token, // Append token
        };
        return updatedMessages;
      });

      readStream(); // Continue reading the stream
    };

    readStream();
  };
  
=======
import {useChat} from "ai/react";

export default function Home() {
  
  const [input, setInput] = useState("");
  const [loading,setLoading] = useState(false)

  const { messages, inputs, handleInputChange, handleSubmit } = useChat({
    api: "http://127.0.0.1:8000/api/chat"
  });
>>>>>>> d73d206e4b4782fb6e92bd20bc2d719d881908cd


  return (
    <div className="flex flex-col min-h-screen">
      <header className="bg-gray-800 text-white text-center py-8">
<<<<<<< HEAD
        <h1 className="text-4xl font-bold">FUNNY DEMO</h1>
=======
        <h1 className="text-4xl font-bold">VERON DEEPCHIP</h1>
>>>>>>> d73d206e4b4782fb6e92bd20bc2d719d881908cd
        {/* <p className="text-lg mt-2">People detection</p> */}
      </header>

      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
       
      
<div className="container mx-auto shadow-lg rounded-lg">
      
    <div className="px-5 py-5 flex justify-between items-center bg-white border-b-2">
      <div className="font-semibold text-2xl">GoingChat</div>
      <div className="w-1/2">
<<<<<<< HEAD
        <p>Hello User, Welcome to Chatbox</p>
=======
        <p>Hello User, Welcome to Veron Chatbox</p>
>>>>>>> d73d206e4b4782fb6e92bd20bc2d719d881908cd
      </div>
      <div
        className="h-12 w-12 p-2 bg-yellow-500 rounded-full text-white font-semibold flex items-center justify-center"
      >
        RA
      </div>
    </div>
    <div className="flex flex-row justify-between bg-white">
      <div className="flex flex-col w-2/5 border-r-2 overflow-y-auto">
        
        <div className="border-b-2 py-4 px-2">
          <input
            type="text"
            placeholder="search chatting"
            className="py-2 px-2 border-2 border-gray-200 rounded-2xl w-full"
          />
        </div>
    
        <div
          className="flex flex-row py-4 px-2 justify-center items-center border-b-2"
        >
          <div className="w-1/4">
            <img
              src="https://source.unsplash.com/_7LbC5J-jw4/600x600"
              className="object-cover h-12 w-12 rounded-full"
              alt=""
            />
          </div>
          <div className="w-full">
            <div className="text-lg font-semibold">Luis1994</div>
            <span className="text-gray-500">Pick me at 9:00 Am</span>
          </div>
        </div>
        <div className="flex flex-row py-4 px-2 items-center border-b-2">
          <div className="w-1/4">
            <img
              src="https://source.unsplash.com/otT2199XwI8/600x600"
              className="object-cover h-12 w-12 rounded-full"
              alt=""
            />
          </div>
          <div className="w-full">
            <div className="text-lg font-semibold">Everest Trip 2021</div>
            <span className="text-gray-500">Hi Sam, Welcome</span>
          </div>
        </div>
        <div
          className="flex flex-row py-4 px-2 items-center border-b-2 border-l-4 border-blue-400"
        >
          <div className="w-1/4">
            <img
              src="https://source.unsplash.com/L2cxSuKWbpo/600x600"
              className="object-cover h-12 w-12 rounded-full"
              alt=""
            />
          </div>
          <div className="w-full">
            <div className="text-lg font-semibold">MERN Stack</div>
            <span className="text-gray-500">Lusi : Thanks Everyone</span>
          </div>
        </div>
        <div className="flex flex-row py-4 px-2 items-center border-b-2">
          <div className="w-1/4">
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-12 w-12 rounded-full"
              alt=""
            />
          </div>
          <div className="w-full">
            <div className="text-lg font-semibold">Javascript Indonesia</div>
            <span className="text-gray-500">Evan : some one can fix this</span>
          </div>
        </div>
        <div className="flex flex-row py-4 px-2 items-center border-b-2">
          <div className="w-1/4">
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-12 w-12 rounded-full"
              alt=""
            />
          </div>
          <div className="w-full">
            <div className="text-lg font-semibold">Javascript Indonesia</div>
            <span className="text-gray-500">Evan : some one can fix this</span>
          </div>
        </div>

        <div className="flex flex-row py-4 px-2 items-center border-b-2">
          <div className="w-1/4">
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-12 w-12 rounded-full"
              alt=""
            />
          </div>
          <div className="w-full">
            <div className="text-lg font-semibold">Javascript Indonesia</div>
            <span className="text-gray-500">Evan : some one can fix this</span>
          </div>
        </div>
      
      </div>
      
      <div className="w-full px-5 flex flex-col justify-between">
        <div className="flex flex-col mt-5">
<<<<<<< HEAD
        


        {/* <div className="border p-4 h-80 overflow-y-auto"> */}
        {messages.map((msg, index) => (
          <div key={index}> 
            {msg.role == "user" ? <div className="flex justify-end mb-4">
            <div
              className="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
            >
              {msg.content}
            </div>
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-8 w-8 rounded-full"
              alt=""
            />
          </div>:<div className="flex justify-start mb-4">
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-8 w-8 rounded-full"
              alt=""
            />
            <div
              className="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white"
              >
              {msg.content}
            </div>
          </div>}
          </div>
        ))}
      {/* </div> */}

          {/* <div className="flex justify-start mb-4">
=======
          
          <div className="flex justify-start mb-4">
>>>>>>> d73d206e4b4782fb6e92bd20bc2d719d881908cd
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-8 w-8 rounded-full"
              alt=""
            />
            <div
              className="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white"
              >
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat
              at praesentium, aut ullam delectus odio error sit rem. Architecto
              nulla doloribus laborum illo rem enim dolor odio saepe,
              consequatur quas?
            </div>
<<<<<<< HEAD
          </div> */}
          
         
=======
          </div>
          <div className="flex justify-end mb-4">
            <div
              className="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
            >
              Welcome to group everyone !
            </div>
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-8 w-8 rounded-full"
              alt=""
            />
          </div>
          <div className="flex justify-end mb-4">
            <div>
              <div
                className="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
              >
                Lorem ipsum dolor, sit amet consectetur adipisicing elit.
                Magnam, repudiandae.
              </div>

              <div
                className="mt-4 mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl text-white"
              >
                Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Debitis, reiciendis!
              </div>
            </div>
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-8 w-8 rounded-full"
              alt=""
            />
          </div>
          <div className="flex justify-start mb-4">
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              className="object-cover h-8 w-8 rounded-full"
              alt=""
            />
            <div
              className="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl text-white"
            >
              happy holiday guys!
            </div>
          </div>
>>>>>>> d73d206e4b4782fb6e92bd20bc2d719d881908cd
        </div>
        <div className="py-5 flex items-center gap-3">
  <input
    className="w-full bg-gray-300 py-3 px-3 rounded-xl"
    type="text"
    placeholder="Type your message here..."
<<<<<<< HEAD
    onChange={(event)=>{setInput(event.target.value)}}
    value = {input}
  />
  <button className="bg-blue-500 text-white px-5 py-3 rounded-xl"
  onClick={()=>{sendMessage()}}
=======
    onChange={handleInputChange}
    value = {input}
  />
  <button className="bg-blue-500 text-white px-5 py-3 rounded-xl"
  onClick={handleSubmit}
>>>>>>> d73d206e4b4782fb6e92bd20bc2d719d881908cd
  >
    Enter
  </button>
</div>
      </div>
      
      
      </div>
</div>

      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/window.svg"
            alt="Window icon"
            width={16}
            height={16}
          />
          Examples
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Go to nextjs.org →
        </a>
      </footer>
    </div>
  );
}
