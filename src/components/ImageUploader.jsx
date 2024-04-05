import React, { useState } from 'react';
import './ImageUploader.scss';

const ImageUploader = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setSelectedImage(file);
    // Reset prediction when a new image is selected
    setPrediction(null);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    try {
      if (!selectedImage) {
        setError('No image selected');
        return;
      }

      const formData = new FormData();
      formData.append('file', selectedImage);

      fetch('http://localhost:3000/disease_detect', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Server error: ' + response.statusText);
        }
        return response.json();
      })
      .then(data => {
        setPrediction(data['leaf status']);
        setError(null);
      })
      .catch(error => {
        setError('Error: ' + error.message);
      });
    } catch (error) {
      setError('Error: ' + error.message);
    }
  };

  return (
    <div className="image-uploader-container">
      <div className="image-uploader">
        <h2>Upload Image</h2>
        <form onSubmit={handleSubmit}>
          <input type="file" accept="image/*" onChange={handleImageChange} />
          <button type="submit">Upload</button>
        </form>
        {error && <p className="error-message">{error}</p>}
        {selectedImage && (
          <div className="preview-container">
            <h3>Preview:</h3>
            <img src={URL.createObjectURL(selectedImage)} alt="Preview" />
            {prediction && (
              <div>
                <h3>Prediction:</h3>
                <p>{prediction}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUploader;
