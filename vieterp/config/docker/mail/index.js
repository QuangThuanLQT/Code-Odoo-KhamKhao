const nodemailer = require('nodemailer');
const MailDev = require('maildev');
const config  = require('./config.json');

const maildev = new MailDev();

maildev.listen();

maildev.on('new', function (email) {
    const createEmail = function(data) {
        const headers = data['headers'];
        const msgText = data['text'];
        const msgHtml = data['text'];

        const message = {
            from: 'noreply@vieterp.net',
            to: headers['to'],
            subject: headers['subject'],
            text: msgText,
            html: msgHtml
        };
        console.log('message', message);
        return message;
    };

    // Send email.
    const message = createEmail(email);
    var transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'thethaosi.sms@gmail.com',
            pass: '12341234abcd@'
        }
    });

    transporter.sendMail(message, function (err, info) {
        if(err) {
            console.log(err)
        } else {
            console.log(info);
        }
    });
});