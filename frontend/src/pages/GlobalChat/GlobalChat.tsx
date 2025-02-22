import { useState, useEffect } from "react";

const GlobalChat = () => {
    // State to store the input value
    const [messageText, setMessageText] = useState<string>("");
    const [messages, setMessages] = useState<IMessage[]>([]);
    const [socketState, setSocketState] = useState<number | null>(null);

    const username = "test"; // TODO: Put the user's actual user id here
    const token = "1"   // TODO: I imagine this could be some kind of auth thing

    const [socket, setSocket] = useState<WebSocket | null>(null);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMessageText(e.target.value);
    };

    const handleSendClick = () => {
        const message: IMessage = {
            text: messageText,
            timestamp: Date.now(),
            username: username
        };
        setMessageText(""); // Clear input after sending
        socket?.send(JSON.stringify(message));
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            handleSendClick();
        }
    };

    useEffect(() => {
        const newSocket = new WebSocket("ws://localhost:8000/ws/"+token);
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
