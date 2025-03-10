import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.apiKey
})
 
 async function main() {

   const list = await openai.files.list();
 
   for await (const file of list) {
     console.log(file.id);
     await openai.files.del(file.id);
   }

 }
 
 main();