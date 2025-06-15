// Main JavaScript for CodeCraft AI

document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runBtn');
    const languageSelect = document.getElementById('languageSelect');
    const aiGenerateBtn = document.getElementById('aiGenerateBtn');
    const aiPrompt = document.getElementById('aiPrompt');
    const aiResponse = document.getElementById('aiResponse');
    const output = document.getElementById('output');
    let websocket;

    // Initialize WebSocket connection
    function initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = `${protocol}${window.location.host}/ws`;
        
        websocket = new WebSocket(wsUrl);
        
        websocket.onopen = () => {
            console.log('WebSocket connected');
        };
        
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };
        
        websocket.onclose = () => {
            console.log('WebSocket disconnected');
            // Attempt to reconnect after 5 seconds
            setTimeout(initWebSocket, 5000);
        };
    }

    // Handle incoming WebSocket messages
    function handleWebSocketMessage(data) {
        if (data.type === 'output') {
            output.textContent += data.content + '\n';
            output.scrollTop = output.scrollHeight;
        } else if (data.type === 'ai_response') {
            showAIResponse(data.content);
        } else if (data.type === 'error') {
            output.textContent += `Error: ${data.content}\n`;
            output.scrollTop = output.scrollHeight;
        }
    }

    // Run code
    async function runCode() {
        const code = editor.getValue();
        const language = languageSelect.value;
        
        output.textContent = 'Running...\n';
        
        try {
            const response = await fetch('/api/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code,
                    language
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                output.textContent = `Error: ${result.error}\n`;
            } else {
                output.textContent = result.output || 'No output';
            }
        } catch (error) {
            output.textContent = `Error: ${error.message}\n`;
        }
        
        output.scrollTop = output.scrollHeight;
    }

    // Generate code with AI
    async function generateCode() {
        const prompt = aiPrompt.value.trim();
        if (!prompt) return;
        
        const language = languageSelect.value;
        const currentCode = editor.getValue();
        
        aiResponse.textContent = 'AI is thinking...';
        aiResponse.classList.remove('hidden');
        aiGenerateBtn.disabled = true;
        
        try {
            const response = await fetch('/api/ai/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt,
                    language,
                    currentCode
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                showAIResponse(`Error: ${result.error}`, true);
            } else {
                showAIResponse(result.response);
            }
        } catch (error) {
            showAIResponse(`Error: ${error.message}`, true);
        } finally {
            aiGenerateBtn.disabled = false;
        }
    }
    
    // Show AI response in a formatted way
    function showAIResponse(response, isError = false) {
        aiResponse.innerHTML = '';
        
        if (isError) {
            aiResponse.innerHTML = `<div class="text-red-400">${response}</div>`;
            return;
        }
        
        // Check if the response contains code blocks
        if (response.includes('```')) {
            // Split by code blocks
            const parts = response.split(/```(\w*)\n?([\s\S]*?)```/g);
            
            for (let i = 0; i < parts.length; i += 3) {
                // Add text before code block
                if (i > 0 || parts[i].trim() !== '') {
                    const text = document.createElement('div');
                    text.className = 'mb-2';
                    text.textContent = parts[i];
                    aiResponse.appendChild(text);
                }
                
                // Add code block if it exists
                if (i + 1 < parts.length) {
                    const language = parts[i + 1] || '';
                    const code = parts[i + 2] || '';
                    
                    const codeBlock = document.createElement('pre');
                    codeBlock.className = 'bg-gray-700 p-3 rounded mb-4 overflow-x-auto';
                    
                    const codeElement = document.createElement('code');
                    codeElement.className = `language-${language}`;
                    codeElement.textContent = code;
                    
                    const copyBtn = document.createElement('button');
                    copyBtn.className = 'float-right bg-gray-600 hover:bg-gray-500 text-white text-xs px-2 py-1 rounded';
                    copyBtn.textContent = 'Copy';
                    copyBtn.onclick = () => {
                        navigator.clipboard.writeText(code);
                        copyBtn.textContent = 'Copied!';
                        setTimeout(() => {
                            copyBtn.textContent = 'Copy';
                        }, 2000);
                    };
                    
                    const insertBtn = document.createElement('button');
                    insertBtn.className = 'float-right bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-2 py-1 rounded mr-2';
                    insertBtn.textContent = 'Insert';
                    insertBtn.onclick = () => {
                        editor.setValue(editor.getValue() + '\n' + code);
                        insertBtn.textContent = 'Inserted!';
                        setTimeout(() => {
                            insertBtn.textContent = 'Insert';
                        }, 2000);
                    };
                    
                    codeBlock.appendChild(codeElement);
                    codeBlock.appendChild(document.createElement('br'));
                    codeBlock.appendChild(insertBtn);
                    codeBlock.appendChild(copyBtn);
                    
                    aiResponse.appendChild(codeBlock);
                }
            }
        } else {
            // No code blocks, just show as plain text
            aiResponse.textContent = response;
        }
        
        // Add a button to insert the entire response
        if (response.trim()) {
            const insertAllBtn = document.createElement('button');
            insertAllBtn.className = 'mt-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm px-3 py-1 rounded';
            insertAllBtn.textContent = 'Insert All Code';
            insertAllBtn.onclick = () => {
                const codeBlocks = aiResponse.querySelectorAll('code');
                let allCode = '';
                
                codeBlocks.forEach(block => {
                    allCode += block.textContent + '\n\n';
                });
                
                if (allCode.trim()) {
                    editor.setValue(editor.getValue() + '\n' + allCode);
                    insertAllBtn.textContent = 'Inserted!';
                    setTimeout(() => {
                        insertAllBtn.textContent = 'Insert All Code';
                    }, 2000);
                }
            };
            
            aiResponse.appendChild(document.createElement('br'));
            aiResponse.appendChild(insertAllBtn);
        }
    }

    // Event Listeners
    runBtn.addEventListener('click', runCode);
    aiGenerateBtn.addEventListener('click', generateCode);
    
    // Handle Ctrl+Enter to run code
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            runCode();
        }
    });
    
    // Initialize WebSocket
    initWebSocket();
    
    // Set focus to editor on load
    editor.focus();
});
