const sgMail = require('@sendgrid/mail');
const humanizeDuration = require('humanize-duration');
const axios = require('axios');
const config = require('./config.json');

// subscribeMailgun is the main function called by Cloud Functions.
module.exports.subscribeNotification = (pubSubEvent, context) => {
    const build = eventToBuild(pubSubEvent.data);

  // Skip if the current status is not in the status list.
    const status = ['SUCCESS', 'FAILURE', 'INTERNAL_ERROR', 'TIMEOUT'];
    if (status.indexOf(build.status) === -1) {
        return;
    }

    // Send email.
    const message = createMessage(build);

    sgMail.setApiKey(config.SENDGRID_API_KEY);
    sgMail.send(message);

    sendTelegramMessage(message);
};

// eventToBuild transforms pubsub event message to a build object.
const eventToBuild = (data) => {
    return JSON.parse(Buffer.from(data, 'base64').toString());
};

// createEmail creates an email message from a build object.
const createMessage = (build) => {
    const duration = humanizeDuration(new Date(build.finishTime) - new Date(build.startTime));
    const msgText = `Build ${build.id} finished with status ${build.status}, in ${duration}.`;
    let msgHtml = `<p>${msgText}</p><p><a href="${build.logUrl}">Build logs</a></p>`;
    if (build.images) {
        const images = build.images.join(',');
        msgHtml += `<p>Images: ${images}</p>`;
    }
    const message = {
        from: config.EMAIL_FROM,
        to: config.EMAIL_TO,
        subject: `Build ${build.id} finished`,
        text: msgText,
        html: msgHtml
    };
    return message;
};

const sendTelegramMessage = (message) => {
    const token = config.TELEGRAM_TOKEN;
    const url = 'https://api.telegram.org/bot' + token + '/sendMessage';

    axios.post(url, {
        chat_id: config.TELEGRAM_CHAT_ID,
        text: message.html,
    })
    .then(function (response) {
        console.log(response);
        // res.send({ status: 'OK'});
    })
    .catch(function (error) {
        console.log(error);
        // res.sendStatus(500);
    });
};