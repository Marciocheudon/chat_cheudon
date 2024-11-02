// lib/providers/chat_provider.dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_tts/flutter_tts.dart';

class ChatProvider extends ChangeNotifier {
  List<Message> _messages = [];

  List<Message> get messages => _messages;

  final String _apiUrl = 'http://192.168.56.1:8000/ask';

  final FlutterTts _flutterTts = FlutterTts();

  ChatProvider() {
    // Configurações iniciais do TTS
    _flutterTts.setLanguage('pt-BR');
    _flutterTts.setPitch(1.0); // Ajusta o tom da voz
    _flutterTts.setSpeechRate(0.5); // Ajusta a velocidade da fala
  }

  Future<void> sendMessage(String text) async {
    if (text.isEmpty) return;

    // Adiciona a mensagem do usuário à lista
    _messages.add(Message(text: text, isUser: true));
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse(_apiUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'question': text}),
      );

      // Log do corpo bruto da resposta
      print('Raw response body: ${response.body}');

      if (response.statusCode == 200) {
        // Decodifica corretamente o corpo da resposta usando UTF-8
        final responseBody = utf8.decode(response.bodyBytes);
        final data = jsonDecode(responseBody);
        String reply = data['response'];

        // Log da resposta decodificada
        print('Decoded reply: $reply');

        // Adiciona a resposta do modelo à lista
        _messages.add(Message(text: reply, isUser: false));
        notifyListeners();

        // Fala a resposta usando TTS
        await _speak(reply);
      } else {
        // Lida com erros da API
        _messages.add(Message(
          text: 'Desculpe, ocorreu um erro ao obter a resposta.',
          isUser: false,
        ));
        notifyListeners();
      }
    } catch (e) {
      // Lida com erros de conexão
      _messages.add(Message(
        text: 'Não foi possível se conectar ao servidor.',
        isUser: false,
      ));
      notifyListeners();
    }
  }

  Future<void> _speak(String text) async {
    await _flutterTts.stop(); // Para qualquer fala em andamento
    await _flutterTts.speak(text);
  }
}

class Message {
  final String text;
  final bool isUser;

  Message({required this.text, required this.isUser});
}
