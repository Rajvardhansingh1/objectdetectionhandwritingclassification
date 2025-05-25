import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'api_service.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  _MyAppState createState() => _MyAppState();
}
class _MyAppState extends State<MyApp> {
  File? _image;
  String _result = "";
  final ApiService _apiService = ApiService();

  Future<void> _pickImage() async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.gallery);

   if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  Future<void> _processImage(String mode) async {
    if (_image == null) return;
    try {
      var response = await _apiService.uploadImage(_image!, mode);
      setState(() {
        _result = response.toString();
      });
    } catch (e) {
      setState(() {
        _result = "Error: ${e.toString()}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("AI Image Processing")),
        body: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _image != null ? Image.file(_image!) : Text("No image selected"),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () => _processImage("object_detection"),
                  child: Text("Object Detection"),
                ),
                SizedBox(width: 10),
                ElevatedButton(
                  onPressed: () => _processImage("handwriting"),
                  child: Text("Handwriting OCR"),
                ),
              ],
            ),
            Padding(
              padding: EdgeInsets.all(16.0),
              child: Text("Result: $_result"),
            ),
            ElevatedButton(
              onPressed: _pickImage,
              child: Text("Pick Image"),
            ),
          ],
        ),
      ),
    );
  }
}
