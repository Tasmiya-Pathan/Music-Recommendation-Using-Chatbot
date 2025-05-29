const sendChatBtn = document.querySelector(".chat-input span");
const chatInput = document.querySelector(".chat-input textarea");
const chatbox = document.querySelector(".chatbox");
const getRecommBtm = document.querySelector(".btn-recom")

let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;
let userAllMessages = "";
const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li")
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? '<p></p>' : '<span class="material-symbols-outlined">smart_toy</span> <p></p>';
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi;
}

const generateResponse = async (chatElement) => {
    const function_name = 'responsed';  // Set the desired function name
    const param1 = userMessage;
    const messageElement = chatElement.querySelector("p");

    fetch('tone_analyser/'+function_name+'/'+param1+'').then((response)=> response.json()).then((data) => {
        messageElement.textContent = data.output.output
    }).catch((error) => console.error('Error fetching paragraph: ', error));
}

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if(!userMessage) return;
    userAllMessages = userAllMessages + ". " +userMessage
    chatInput.value = "";
    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

const displayRecommendations = (recommendations) => {
    const tbody = document.querySelector('.show-table tbody');

    // Clear existing rows
    tbody.innerHTML = '';


    // Exclude 'emotion' from the list of keys
    const songKeys = Object.keys(recommendations).filter(key => key !== 'emotion');
    console.log(songKeys)

    // Iterate over the song keys
    songKeys.forEach(function(key) {
        const row = document.createElement('tr');

        // Create a cell for the song name
        const nameCell = document.createElement('td');
        nameCell.textContent = key;

        // Create a cell for the URL
        const urlCell = document.createElement('td');
        const urlLink = document.createElement('a');
        urlLink.textContent = recommendations[key];
        urlCell.appendChild(urlLink);

        // Append cells to the row and row to the tbody
        row.appendChild(nameCell);
        row.appendChild(urlCell);
        tbody.appendChild(row);
    });
};


const getRecomm = async () => {
    const function_name = 'song_emotion';  // Set the desired function name
    const param1 = userAllMessages;

    fetch('tone_analyser/'+function_name+'/'+param1+'').then((response)=> response.json()).then((data) => {
        console.log(data.output)
        displayRecommendations(data.output);
        const show_r = document.querySelector(".show-recomm")
        show_r.style.visibility = 'visible'
}).catch((error) => console.error('Error fetching paragraph: ', error));


}

sendChatBtn.addEventListener("click", handleChat);
getRecommBtm.addEventListener("click",getRecomm)