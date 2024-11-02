// lib/screens/home_screen.dart
import 'package:cheudon_app/providers/chat_provider.dart';
import 'package:cheudon_app/widgets/input_fiel.dart';
import 'package:cheudon_app/widgets/message_bubble.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final chatProvider = Provider.of<ChatProvider>(context);
    return Scaffold(
      appBar: AppBar(
        title: Text('Assistente Pessoal'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: chatProvider.messages.length,
              itemBuilder: (context, index) {
                final message = chatProvider.messages[index];
                return MessageBubble(
                  text: message.text,
                  isUser: message.isUser,
                );
              },
            ),
          ),
          InputField(),
        ],
      ),
    );
  }
}
