document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const generateUpdateBtn = document.getElementById('generate-update-btn');
    const sendEmailBtn = document.getElementById('send-email-btn');
    const addTopicBtn = document.getElementById('add-topic-btn');
    const newTopicInput = document.getElementById('new-topic-input');
    const updatesList = document.getElementById('updates-list');
    const topicsList = document.getElementById('topics-list');
    const updateDetails = document.getElementById('update-details');
    const updateTimestamp = document.getElementById('update-timestamp');
    const updateChats = document.getElementById('update-chats');
    const updateMaterials = document.getElementById('update-materials');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Load initial data
    loadUpdates();
    loadTopics();
    
    // Event listeners
    generateUpdateBtn.addEventListener('click', generateUpdate);
    sendEmailBtn.addEventListener('click', sendEmailUpdate);
    addTopicBtn.addEventListener('click', addTopic);
    
    // Functions
    async function loadUpdates() {
        try {
            updatesList.innerHTML = '<p class="loading">Loading updates...</p>';
            
            const response = await fetch('/api/updates');
            const updates = await response.json();
            
            if (updates.length === 0) {
                updatesList.innerHTML = '<p>No updates found. Generate your first update!</p>';
                return;
            }
            
            updatesList.innerHTML = '';
            updates.forEach(update => {
                const updateItem = document.createElement('div');
                updateItem.className = 'list-item';
                updateItem.dataset.filename = update.filename;
                
                const timestamp = new Date(update.timestamp);
                
                updateItem.innerHTML = `
                    <div class="list-item-title">Update from ${timestamp.toLocaleDateString()}</div>
                    <div class="list-item-subtitle">
                        ${update.num_chats} chats, ${update.num_updates} new materials
                    </div>
                `;
                
                updateItem.addEventListener('click', () => loadUpdateDetails(update.filename));
                
                updatesList.appendChild(updateItem);
            });
        } catch (error) {
            console.error('Error loading updates:', error);
            updatesList.innerHTML = '<p>Error loading updates. Please try again.</p>';
        }
    }
    
    async function loadTopics() {
        try {
            topicsList.innerHTML = '<p class="loading">Loading topics...</p>';
            
            const response = await fetch('/api/topics');
            const topics = await response.json();
            
            if (topics.length === 0) {
                topicsList.innerHTML = '<p>No topics found. Add your first topic!</p>';
                return;
            }
            
            topicsList.innerHTML = '';
            topics.forEach(topic => {
                const topicItem = document.createElement('div');
                topicItem.className = 'list-item';
                
                const lastUpdated = new Date(topic.last_updated);
                
                topicItem.innerHTML = `
                    <div class="list-item-title">${topic.name}</div>
                    <div class="list-item-subtitle">
                        Last checked: ${lastUpdated.toLocaleDateString()}, 
                        ${topic.sources.length} sources, 
                        ${topic.new_materials.length} new materials
                    </div>
                `;
                
                topicsList.appendChild(topicItem);
            });
        } catch (error) {
            console.error('Error loading topics:', error);
            topicsList.innerHTML = '<p>Error loading topics. Please try again.</p>';
        }
    }
    
    async function loadUpdateDetails(filename) {
        try {
            showLoading();
            
            const response = await fetch(`/api/updates/${filename}`);
            const updateData = await response.json();
            
            // Update timestamp
            const timestamp = new Date(updateData.timestamp);
            updateTimestamp.textContent = `Generated on ${timestamp.toLocaleString()}`;
            
            // Update chats
            updateChats.innerHTML = '';
            if (updateData.chats && updateData.chats.length > 0) {
                updateData.chats.forEach(chat => {
                    const chatDate = new Date(chat.created_at);
                    
                    const chatItem = document.createElement('div');
                    chatItem.className = 'detail-item';
                    chatItem.innerHTML = `
                        <div class="detail-title">${chat.title}</div>
                        <div class="detail-subtitle">${chatDate.toLocaleString()}</div>
                        <div class="detail-content">
                            <p>Topics: ${chat.topics && chat.topics.length > 0 ? chat.topics.join(', ') : 'No topics extracted'}</p>
                            <p>Messages: ${chat.messages ? chat.messages.length : 0}</p>
                        </div>
                    `;
                    
                    updateChats.appendChild(chatItem);
                });
            } else {
                updateChats.innerHTML = '<p>No recent chats found.</p>';
            }
            
            // Update materials
            updateMaterials.innerHTML = '';
            if (updateData.topic_updates && Object.keys(updateData.topic_updates).length > 0) {
                for (const [topic, materials] of Object.entries(updateData.topic_updates)) {
                    const topicItem = document.createElement('div');
                    topicItem.className = 'detail-item';
                    
                    let materialsHtml = '';
                    if (materials && materials.length > 0) {
                        materialsHtml = '<div class="materials-list">';
                        materials.forEach(material => {
                            let materialDate = material.date || 'Unknown date';
                            if (typeof materialDate === 'string' && materialDate !== 'Unknown date') {
                                try {
                                    materialDate = new Date(materialDate).toLocaleDateString();
                                } catch (e) {
                                    // Keep as is if parsing fails
                                }
                            }
                            
                            materialsHtml += `
                                <div class="material-item">
                                    <div class="material-title">${material.title || 'Untitled'}</div>
                                    <div class="material-date">Published: ${materialDate}</div>
                                    <p>${material.snippet || 'No description available'}</p>
                                    <a href="${material.link || '#'}" target="_blank">Read More</a>
                                </div>
                            `;
                        });
                        materialsHtml += '</div>';
                    } else {
                        materialsHtml = '<p>No new materials found for this topic.</p>';
                    }
                    
                    topicItem.innerHTML = `
                        <div class="detail-title">${topic}</div>
                        <div class="detail-content">
                            ${materialsHtml}
                        </div>
                    `;
                    
                    updateMaterials.appendChild(topicItem);
                }
            } else {
                updateMaterials.innerHTML = '<p>No new research materials found.</p>';
            }
            
            // Show the details section
            updateDetails.style.display = 'block';
            
            // Scroll to the details section
            updateDetails.scrollIntoView({ behavior: 'smooth' });
            
            hideLoading();
        } catch (error) {
            console.error('Error loading update details:', error);
            hideLoading();
            alert('Error loading update details. Please try again.');
        }
    }
    
    async function generateUpdate() {
        try {
            showLoading();
            
            const response = await fetch('/api/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const updateData = await response.json();
            
            // Reload updates list
            await loadUpdates();
            
            // Load the new update details
            const filename = `update_${new Date().toISOString().replace(/[:.]/g, '')}.json`;
            await loadUpdateDetails(filename);
            
            hideLoading();
        } catch (error) {
            console.error('Error generating update:', error);
            hideLoading();
            alert('Error generating update. Please try again.');
        }
    }
    
    async function sendEmailUpdate() {
        try {
            showLoading();
            
            const response = await fetch('/api/email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const result = await response.json();
            
            hideLoading();
            
            if (result.status === 'success') {
                alert('Email sent successfully!');
            } else {
                alert(`Failed to send email: ${result.message}`);
            }
        } catch (error) {
            console.error('Error sending email:', error);
            hideLoading();
            alert('Error sending email. Please try again.');
        }
    }
    
    async function addTopic() {
        const topicName = newTopicInput.value.trim();
        
        if (!topicName) {
            alert('Please enter a topic name.');
            return;
        }
        
        try {
            showLoading();
            
            const response = await fetch('/api/topics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: topicName
                })
            });
            
            const result = await response.json();
            
            // Clear the input
            newTopicInput.value = '';
            
            // Reload topics list
            await loadTopics();
            
            hideLoading();
        } catch (error) {
            console.error('Error adding topic:', error);
            hideLoading();
            alert('Error adding topic. Please try again.');
        }
    }
    
    function showLoading() {
        loadingOverlay.style.display = 'flex';
    }
    
    function hideLoading() {
        loadingOverlay.style.display = 'none';
    }
});