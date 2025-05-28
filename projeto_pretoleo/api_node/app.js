const express = require('express');
const axios = require('axios');
const redisClient = require('./redisClient');
const app = express();
app.use(express.json());

app.get('/sensor-data', async (req, res) => {
  const cached = await redisClient.get('sensor-data');
  if (cached) return res.json(JSON.parse(cached));

  const data = {
    temperatura: (20 + Math.random() * 30).toFixed(2),
    pressao: (1000 + Math.random() * 50).toFixed(2)
  };

  await redisClient.set('sensor-data', JSON.stringify(data), { EX: 30 });
  res.json(data);
});

app.post('/alert', async (req, res) => {
  try {
    await axios.post('http://localhost:5000/event', req.body);
    res.send('Alerta enviado com sucesso!');
  } catch (err) {
    res.status(500).send('Erro ao enviar alerta.');
  }
});

app.listen(3000, () => console.log('Node API ouvindo na porta 3000'));
