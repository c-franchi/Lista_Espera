const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

// Cria um novo cliente de WhatsApp
const client = new Client({
    authStrategy: new LocalAuth()
});

// Exibe o QR code no terminal para autenticação
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Client is ready!');
});

// Envia uma mensagem quando o cliente estiver pronto
client.on('ready', () => {
    const number = "5516997813038"; // Substitua pelo número de telefone no formato internacional
    const message = "O candidato foi chamado para o teste prático.";
    const chatId = `${number}@c.us`;

    client.sendMessage(chatId, message).then(response => {
        console.log("Mensagem enviada com sucesso!");
    }).catch(err => {
        console.error("Erro ao enviar mensagem:", err);
    });
});

client.initialize();

