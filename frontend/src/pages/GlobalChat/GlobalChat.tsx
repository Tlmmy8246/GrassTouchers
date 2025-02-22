import { useState, useEffect } from "react";
import { useUserStore } from "store/useUserStore";
import tokenService from 'utils/token'

const GlobalChat = () => {
    // State to store the input value
    const [messageText, setMessageText] = useState<string>("");
    const [messages, setMessages] = useState<IMessage[]>([]);
    const [socketState, setSocketState] = useState<number | null>(null);
    const [socket, setSocket] = useState<WebSocket | null>(null);
    
    const userData = useUserStore(state => state.user);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMessageText(e.target.value);
    };

    const handleSendClick = () => {
        if (userData != null) {
            const message: IMessage = {
                text: messageText,
                timestamp: Date.now(),
                username: userData.username
            };
            const authenticatedMessage = {
                "message": message,
                "token": tokenService.getAccessToken()
            }
            setMessageText(""); // Clear input after sending
            socket?.send(JSON.stringify(authenticatedMessage));
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            handleSendClick();
        }
    };

    useEffect(() => {
        const newSocket = new WebSocket("ws://localhost:8000/ws");
        newSocket.addEventListener("message", (event) => {
            const message = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, message]);
        });
        newSocket.addEventListener("open", (event) => {
            setSocketState(WebSocket.OPEN);
        });
        newSocket.addEventListener("error", () => {
            setSocketState(WebSocket.CLOSING); 
        });
        newSocket.addEventListener("close", () => {
            setSocketState(WebSocket.CLOSED);
        });
        setSocket(newSocket);
        return () => {
            if (newSocket) {
                newSocket.close();
            }
        };
    }, []);

    return (
        <div>
            <h1>Global Chat</h1>

            {socket?.readyState !== WebSocket.OPEN ? (
                <p>Connection not established</p>
            ) : (
                <p></p>
            )}
            <>
                {/* Display the list of messages */}
                <div>
                    {messages.length > 0 ? (
                        messages.map((msg, index) => (
                            <div key={index}>
                                <strong>{msg.username}:</strong> {msg.text}
                            </div>
                        ))
                    ) : (
                        <p>No messages yet</p>
                    )}
                </div>

                {/* Input and Send button */}
                <input
                    type="text"
                    value={messageText} // Bind input value to state
                    onChange={handleInputChange} // Update state on input change
                    onKeyDown={handleKeyDown}
                />
                <button onClick={handleSendClick}>Send</button>
            </>
        </div>
    );
};

export default GlobalChat;
