console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')

presigned_url__get = 'https://s3.eu-west-2.amazonaws.com/470426667096--temp-data--eu-west-2/temp_file_uploads/b6668ea6-6cf8-4218-904c-ceb622d2c1ae?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAW3B45JBMCHI55R5F%2F20240507%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240507T213902Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3ee424e52985b6df723bda3404573b54603983b0c9ad8e2ec79c03e3dcfafdc3'
presigned_url__put = 'https://s3.eu-west-2.amazonaws.com/470426667096--temp-data--eu-west-2/temp_file_uploads/b6668ea6-6cf8-4218-904c-ceb622d2c1ae?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAW3B45JBMCHI55R5F%2F20240507%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240507T213902Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e2f358ae6f41ff9db4f3e5f94bbd885d184448a681b279de2a424a0d216b7aa6'


function uploadString(url, content) {
    const blob = new Blob([content], {type: 'text/plain'});

    fetch(url, { method: 'PUT',
                     body: blob,
                     headers: { 'Content-Type': 'text/plain' }})
        .then(response =>
            {
                if (response.ok) {
                    console.log('Content uploaded successfully, you can open the file at');
                    console.log(presigned_url__get)
                } else {
                    console.log('Failed to upload content');
                }})
    .catch(error => console.error('Error uploading content:', error));
}

// Usage example
const content = "NEW CONTENT Hello, this is the content I want to upload!";
uploadString(presigned_url__put, content);