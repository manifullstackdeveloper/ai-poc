import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.apiKey
})
 
 async function main() {

    const myAssistants = await openai.beta.assistants.list();

     for await (const assistant of myAssistants) {
      console.log(assistant.id);
      const delassistant = await openai.beta.assistants.del(
        assistant.id
      );
      console.log(delassistant);
    }

 }
 
 main();