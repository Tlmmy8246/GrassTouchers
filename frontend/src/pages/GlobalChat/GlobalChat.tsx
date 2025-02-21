import { endpoints } from "global/endpoints";
import http from "utils/https";
import { useState } from "react";

const GlobalChat = () => {
    // State to store the input value
    const [messageText, setMessageText] = useState<string>("");

    const sendMessage = (message: IMessage) => {
        http().post(endpoints.chat.global.messages, message);
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMessageText(e.target.value); // Update the state with the input value
    };

    const handleSendClick = () => {
        const message: IMessage = { 
            text: messageText,
            timestamp: Date.now(),
            uid: "user1"
        }; // Create message object
        sendMessage(message); 
        setMessageText(""); 
    };

    return (
        <div>
            <input
                type="text"
                value={messageText} // Bind input value to state
                onChange={handleInputChange} // Update state on input change
            />
            <button onClick={handleSendClick}>Send</button>
        </div>
    );
}

export default GlobalChat;
