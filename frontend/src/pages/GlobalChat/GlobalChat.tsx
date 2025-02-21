import { endpoints } from "global/endpoints";
import http from "utils/https";
import { useState } from "react";

const GlobalChat = () => {
    // State to store the input value
    const [messageText, setMessageText] = useState<string>("");

    // Function to handle sending the message
    const sendMessage = (message: IMessage) => {
        // Do the API call
        http().post(endpoints.chat.global.messages, message);
    };

    // Handle input change
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMessageText(e.target.value); // Update the state with the input value
    };

    // Handle button click (send the message)
    const handleSendClick = () => {
        const message: IMessage = { 
            text: messageText,
            timestamp: Date.now(),
            uid: "user1"
        }; // Create message object
        sendMessage(message); // Call the send function with the message
        setMessageText(""); // Optionally clear the input after sending
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
