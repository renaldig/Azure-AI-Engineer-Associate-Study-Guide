curl --location --request POST '<endpoint>/contentsafety/text:detectProtectedMaterial?api-version=2023-10-15-preview' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "text": " In the land of dreams where shadows dance, the moonlight sings a lullaby of chance. Stars whisper secrets to the silent night, as the winds of change carry whispers bright"
}'
