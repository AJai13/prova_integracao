<?php
if ($_SERVER['REQUEST_METHOD'] === 'GET' && $_SERVER['REQUEST_URI'] === '/equipments') {
    echo json_encode(['bomba', 'valvula', 'turbina']);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_SERVER['REQUEST_URI'] === '/dispatch') {
    $conn = new AMQPConnection([
        'host' => 'localhost',
        'port' => 5672,
        'login' => 'guest',
        'password' => 'guest',
        'vhost' => '/'
    ]);
    $conn->connect();
    $ch = new AMQPChannel($conn);
    $q = new AMQPQueue($ch);
    $q->setName('logistica');
    $q->setFlags(AMQP_DURABLE);  
    $q->setFlags(AMQP_PASSIVE);
    $q->declareQueue();
    $ex = new AMQPExchange($ch);
    $ex->setName('amq.direct');
    $ex->setType(AMQP_EX_TYPE_DIRECT);
    $ex->publish('Mensagem urgente de logística', 'logistica', AMQP_NOPARAM);
    echo "Mensagem enviada via RabbitMQ!";
}
?>
