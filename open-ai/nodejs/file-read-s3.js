
import OpenAI from "openai";
import fs from "fs";
import AWS from "aws-sdk";


const openai = new OpenAI({
    apiKey: process.env.apiKey
})

// Function to download file from S3
async function downloadFileFromS3(bucketName, fileKey, filePath) {
    
     const s3 = new AWS.S3({
         region: process.env.region,
         accessKeyId: process.env.accessKeyId,
         secretAccessKey: process.env.secretAccessKey
     });

    const params = {
      Bucket: bucketName,
      Key: fileKey,
    };
    
  
    const file = fs.createWriteStream(filePath);
  
    s3.getObject(params).createReadStream().pipe(file);
  
    return new Promise((resolve, reject) => {
      file.on('finish', resolve);
      file.on('error', reject);
    });

}

async function uploadFileToOpenAI(filePath) {
    try {
        const file = await openai.files.create({
            file: fs.createReadStream(filePath), // File from local system
            purpose: "assistants"
        });

        console.log("File uploaded:", file);
    } catch (error) {
        console.error("Error uploading file:", error);
    }
}

// Main function
async function main() {
    const filePath = 'file.pdf';
    // Alternatively, you can download from S3 (comment out the URL section and use S3 instead)
    const bucketName = process.env.bucketName
    const fileKey = process.env.fileKey
    await downloadFileFromS3(bucketName, fileKey, filePath);
    console.log('File downloaded from S3');
    // Upload the file to OpenAI
    await uploadFileToOpenAI(filePath);
}

main().catch(console.error);