import AWS from 'aws-sdk'

AWS.config.update({accessKeyId: 'AKIAIGI4TJMRN7BX3TSA', secretAccessKey: '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'})
AWS.config.region = 'us-east-2'  //us-east-2 is Ohio

export const database = new AWS.DynamoDB()