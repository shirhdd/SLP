import React, { useState } from 'react';

const DragAndDrop = ({ word }) => {
    const [file, setFile] = useState(null);

    const handleDrop = (e) => {
        e.preventDefault();
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile.type === 'audio/wav') {
            setFile(droppedFile);
        } else {
            alert('Only WAV files are allowed!');
        }
    };

    const handleSubmit = async () => {
        if (file) {
            try {
                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch('http://127.0.0.1:5000/predict', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const result = await response.json(); // Parse response JSON
                    console.log('Response from server:', result);
                }

                if (response.ok) {
                    console.log('File uploaded successfully');
                    // Handle success
                } else {
                    console.error('Failed to upload file');
                    // Handle failure
                }
            } catch (error) {
                console.error('Error uploading file:', error);
                // Handle error
            }
        } else {
            alert('Please drop a WAV file first!');
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    return (
        <div>
            <h2>{word || 'default'}</h2>
            <div
                style={{
                    width: '200px',
                    height: '100px',
                    border: '2px dashed #aaa',
                    borderRadius: '5px',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    marginBottom: '20px',
                }}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
            >
                {file ? (
                    <p>{file.name}</p>
                ) : (
                    <p>Drag your WAV file here</p>
                )}
            </div>
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
};

export default DragAndDrop;
