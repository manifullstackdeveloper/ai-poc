
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

async function readS3File(bucket, key) {
  const params = {
    Bucket: bucket,
    Key: key,
  };

  try {
    const command = new GetObjectCommand(params);
    const response = await s3Client.send(command);

    // Check if the body is a Readable stream
    if (response.Body instanceof Readable) {
        // Use createReadStream to handle the stream
        const stream = response.Body;
        let data = '';
        for await (const chunk of stream) {
          data += chunk;
        }
        return data;
    } else {
      throw new Error('Response body is not a Readable stream.');
    }
  } catch (error) {
    console.error("Error reading file from S3:", error);
    throw error;
  }
}

export const handler = async (event) => {
    const textAll = ""

    try {

      const filePath = '/tmp/file.pdf';
      const bucketName = process.env.bucketName
      const fileKey = process.env.fileKey

      await downloadFileFromS3(bucketName, fileKey, filePath);

      console.log('File downloaded from S3');

      // Upload the file to OpenAI
      await uploadFileToOpenAI(filePath);

      const vectorStore = await openai.beta.vectorStores.create({
          name: "Mani QA"
      });

      const file = await openai.files.create({
          file: fs.createReadStream(filePath),
          purpose: "assistants",
      });
      

      await openai.beta.vectorStores.files.create(vectorStore.id, {
          file_id: file.id
      });

      console.log("Vector Store Created:", vectorStore);

      const assistant = await openai.beta.assistants.create({
          name: "Personal Portfolio Assistant",
          instructions: "....todo",
          model: "gpt-4o-mini",
          tools: [{ type: "file_search" }],
          tool_resources: {
              file_search: {
                vector_store_ids: [vectorStore.id]
              }
          }
      });

      console.log("Assistant Created:", assistant);
      
      const thread = await openai.beta.threads.create({
        messages: [
          {
            role: "user",
            content: "What are the company you worked?",
          }
        ],
      });
      
      // The thread now has a vector store in its tool resources.
      console.log(thread.tool_resources?.file_search);


      const run = await openai.beta.threads.runs.createAndPoll(thread.id, {
          assistant_id: assistant.id,
        });
        
        const messages = await openai.beta.threads.messages.list(thread.id, {
          run_id: run.id,
        });
      
        const message = messages.data.pop();
        //console.log(message);

        if (message.content[0].type === "text") {
            const { text } = message.content[0];
            const { annotations } = text;
            const citations = [];
        
            let index = 0;
            for (let annotation of annotations) {
            text.value = text.value.replace(annotation.text, "[" + index + "]");
            const { file_citation } = annotation;
            if (file_citation) {
                const citedFile = await openai.files.retrieve(file_citation.file_id);
                citations.push("[" + index + "]" + citedFile.filename);
            }
            index++;
          }
      
    
      console.log(text.value);
      console.log(citations.join("\n"));
      textAll = text.value + "\n" + citations.join("\n");
    }

  } catch (error) {   
      console.error("Error creating assistant:", error);
  }

  const response = {
    statusCode: 200,
    body: JSON.stringify(textAll),
  };
  return response;
};
