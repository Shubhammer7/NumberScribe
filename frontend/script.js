const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let painting = false;

canvas.addEventListener('mousedown', startPosition);
canvas.addEventListener('mouseup', endPosition);
canvas.addEventListener('mousemove', draw);

function startPosition(e) {
    painting = true;
    draw(e);
}

function endPosition() {
    painting = false;
    ctx.beginPath();
}

function draw(e) {
    if (!painting) return;
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';
    
    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function predictDigit() {
    try {
        const dataUrl = canvas.toDataURL('image/png');
        console.log('Data URL:', dataUrl);
        
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ image: dataUrl }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        console.log('Received response from backend:', result);
        
        document.getElementById('result').innerText = `Predicted Digit: ${result.digit}, Confidence: ${result.confidence.toFixed(4)}`;
    } catch (error) {
        console.error('Error predicting digit:', error);
    }
}

// Debugging function to show the image on the page
function showImage() {
    const img = new Image();
    img.src = canvas.toDataURL('image/png');
    document.body.appendChild(img);
}
document.getElementById('predictButton').addEventListener('click', showImage);
