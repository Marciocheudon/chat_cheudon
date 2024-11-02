// lib/widgets/input_field.dart
import 'package:cheudon_app/providers/chat_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class InputField extends StatefulWidget {
  @override
  _InputFieldState createState() => _InputFieldState();
}

class _InputFieldState extends State<InputField> {
  final _controller = TextEditingController();
  bool _isSending = false;

  void _sendMessage() async {
    if (_controller.text.trim().isEmpty) return;

    setState(() {
      _isSending = true;
    });

    await Provider.of<ChatProvider>(context, listen: false)
        .sendMessage(_controller.text.trim());

    _controller.clear();

    setState(() {
      _isSending = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Container(
        padding: EdgeInsets.only(left: 8.0, right: 8.0, bottom: 8.0, top: 4.0),
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: _controller,
                decoration: InputDecoration(hintText: 'Digite sua pergunta...'),
                onSubmitted: (_) => _sendMessage(),
              ),
            ),
            _isSending
                ? CircularProgressIndicator()
                : IconButton(
                    icon: Icon(Icons.send),
                    onPressed: _sendMessage,
                  ),
          ],
        ),
      ),
    );
  }
}
