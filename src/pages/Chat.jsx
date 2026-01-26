import React, {useEffect, useState} from 'react'
import {useLocation} from "react-router";
import {getChatResponse} from "../services/openai.js";
import Text from "../components/Inputs/Text.jsx";
import Primary from "../components/Buttons/Primary.jsx";

const Chat = () => {
  const location = useLocation();
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (location.state?.chatInput) {
      setLoading(true);
      getChatResponse(location.state.chatInput)
        .then((result) => {
          setResponse(result);
        })
        .catch((error) => {
          console.error("Error fetching chat response:", error);
          setResponse(null);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [location.state?.chatInput]);

  const handleChatInput = (e) => {
    const {value} = e.target;
    setChatInput(value);
  };

  const [chatInput, setChatInput] = useState("");

  const askQuestion = () => {
    setLoading(true);
    setResponse(null);
    getChatResponse(chatInput)
      .then((result) => {
        setResponse(result);
      })
      .catch((error) => {
        console.error("Error fetching chat response:", error);
        setResponse(null);
      }).finally(
      setLoading(false)
    );
  };

  return (
    <div className="p-4">
      <h1>Chat Assistant</h1>
      {loading && <p>Loading...</p>}
      {response && (
        <div className="mt-4 p-4 border rounded ">
          {typeof response === 'string' ? (
            <p>{response}</p>
          ) : (
            <div>
              <div>Asystent: {JSON.stringify(response.reply, null, 2)}</div>
              <div>
                <div className="my-8">
                  <Text
                    placeholder="Ask another question"
                    name="chat"
                    onChange={handleChatInput}
                  />
                  <Primary
                    text="Ask"
                    className="mt-4 p-2"
                    onClick={askQuestion}
                  />
                </div>
              </div>
            </div>)}
        </div>
      )}
      {!loading && !response && (
        <p>No response available. Please try again.</p>
      )}
    </div>
  )
}

export default Chat
