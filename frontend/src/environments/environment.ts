/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-71rarl-5.us', // the auth0 domain prefix
    audience: 'coffee_shop_api', // the audience set for the auth0 app
    clientId: 'NDZwuEJoygpbJJwk3KEO5F9OBAJbpwzT', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
