# resizer

## Navigation
<!-- TOC -->
- [Navigation](#navigation)
    - [Installation](#installation)
    - [Creating a request](#sample-request)
<!-- /TOC -->

## Installation

This microservice uses a hosted **CloudAMQP** RabbitMQ instance.
To publish messages to an existing service, update environmental variables below:
- CLOUDAMQP_URL
- CLOUDAMQP_HOST

Sample publisher file is in this repo as resize_publish.py.

## Sample Request
```json
{
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Savannah_Cat_portrait.jpg/800px-Savannah_Cat_portrait.jpg",
  "height": 500,
  "width": 500,
  "scale_option": "fill"
 }
 ```
 - **image_url** [String] - URL of Image
 - **height** [Number]  - Height in pixels
 - **width** [Number] - Width in pixels
 - **scale_option** [String] (Optional) - Image resize mode: defaults to *ignore*
     - "fill" : Scales image to lesser width or height
     - "fit" : Scales image to greater width or height
     - "ignore" : Ignores aspect ratio, resizes to exact dimensions
     
## Sample Response
**Success**
```json
{
"image_url": "https://account_name.sirv.com/Uploads/image_id?h=500&w=500&scale.option=fill", 
"success": true
}
```
**Failure**
```json
{
  "success": false, 
  "error_message": "Error parsing JSON format."
}
```
 - **image_url** [String] - URL of Resized Image
 - **success** [Boolean] - Whether the image was successfully resized or not
 - **error_message** [String] - If there is failure in resizing, returns error description
 
 
   
