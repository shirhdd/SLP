import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { ClipLoader } from 'react-spinners';  // Import a spinner from react-spinners

function DragAndDropComponent({word, setScore, setResponse}) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [fileUploaded, setFileUploaded] = useState(false);

    const onDrop = useCallback(acceptedFiles => {
        const file = acceptedFiles[0];
        if (file && file.type === 'audio/wav') {
            setFile(file);
            setError('');
            setFileUploaded(true);
        } else {
            setError('Only WAV files are allowed');
            setFileUploaded(false);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: 'audio/wav',
        multiple: false
    });

    const handleSubmit = async () => {
        if (file) {
            setLoading(true);
            const formData = new FormData();
            formData.append('file', file);
            formData.append('word', word);

            try {
                const response = await axios.post('http://127.0.0.1:5000/predict', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.log(response.data);
                setResponse(response.data)
                // Increment score by 10 upon successful response
                setScore(prevScore => prevScore + 10);
            } catch (error) {
                console.error('Error submitting the file:', error);
                alert('Error submitting the file');
            } finally {
                setLoading(false);
                setFile(null);
                setFileUploaded(false);
            }
        }
    };

    return (
        <div>
            <div {...getRootProps()} style={{
                border: error ? '2px solid red' : '2px dashed gray',
                backgroundColor: fileUploaded ? 'lightgreen' : 'transparent',
                padding: '20px',
                textAlign: 'center'
            }}>
                <input {...getInputProps()} />
                {
                    fileUploaded ?
                        <p>File uploaded successfully, please click submit</p> :
                        isDragActive ?
                            <p>Drop the file here ...</p> :
                            <p>Drag 'n' drop a WAV file here, or click to select a file</p>
                }
                {loading && <ClipLoader color="#000000" />}
            </div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button onClick={handleSubmit} disabled={!file || loading}>Submit</button>
        </div>
    );
}

export default DragAndDropComponent;
