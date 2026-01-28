import React, { useEffect, useState } from "react";
import { useLocation } from "react-router";
import { getChatResponse } from "../services/openai.js";
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
    const { value } = e.target;
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
      })
      .finally(setLoading(false));
  };

  return (
    <div className="p-4">
      <h1>Chat Assistant</h1>
      {loading && <p>Loading...</p>}
      {response && (
        <div className="mt-6 rounded-2xl border border-gray-200 bg-white shadow-sm">
          {typeof response === "string" ? (
            <p className="p-4 text-gray-700 leading-relaxed">{response}</p>
          ) : (
            <div className="p-4 space-y-6">
              <div className="rounded-xl bg-gray-50 p-4">
                <p className="mb-2 text-sm font-semibold text-gray-500">
                  Assistant
                </p>
                <pre className="whitespace-pre-wrap text-sm text-gray-800">
                  {JSON.stringify(response.reply, null, 2)}
                </pre>
              </div>
              <div className="space-y-3 border-t pt-4">
                <Text
                  placeholder="Ask another question"
                  name="chat"
                  onChange={handleChatInput}
                />

                <Primary
                  text="Ask"
                  onClick={askQuestion}
                  className="w-full rounded-xl bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
                />
              </div>
            </div>
          )}
        </div>
      )}
      {!loading && !response && <p>No response available. Please try again.</p>}
    </div>
  );
};

export default Chat;
