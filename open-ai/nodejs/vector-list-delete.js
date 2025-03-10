import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.apiKey
})
 
 
 async function main() {

   const vectorStores = await openai.beta.vectorStores.list();

   for await (const vector of vectorStores) {
      console.log(vector.id);
      const deletedVectorStore = await openai.beta.vectorStores.del(
        vector.id
      );
      console.log(deletedVectorStore);
    }

 }
 
 main();