import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://192.168.1.6:8000"; // your FastAPI IP

  Future<Map<String, dynamic>> uploadImage(File imageFile, String mode) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/process/?mode=$mode'),
    );

    request.files.add(await http.MultipartFile.fromPath('file', imageFile.path));
    var response = await request.send();

    if (response.statusCode == 200) {
      var responseData = await response.stream.bytesToString();
      return jsonDecode(responseData);
    } else {
      throw Exception('Failed to process image');
    }
  }
}
