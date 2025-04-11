const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const morgan = require('morgan');
const authRoutes = require('./routes/auth');

dotenv.config();

const app = express();

// Проверка переменных окружения
if (!process.env.MONGO_URI) {
    console.error('Ошибка: MONGO_URI не задана в переменных окружения');
    process.exit(1); // Завершение процесса с ошибкой
}

// Настройка CORS
app.use(cors({
    origin: 'http://localhost:3000', // Разрешаем только запросы с этого источника
    methods: ['GET', 'POST', 'PUT', 'DELETE'], // Разрешаем необходимые методы
    credentials: true // Если нужно передавать куки
}));

app.use(express.json());
app.use(morgan('dev')); // Логирование запросов в режиме разработки

// Подключение к MongoDB
mongoose
    .connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Подключено к MongoDB'))
    .catch((err) => console.error('Ошибка подключения к MongoDB:', err));

// Маршруты
app.use('/api/auth', authRoutes);

// Глобальный обработчик ошибок
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Что-то пошло не так!');
});

const PORT = process.env.PORT || 8000; // Убедитесь, что порт установлен на 8000
app.listen(PORT, () => console.log(`Сервер запущен на порту ${PORT}`));
