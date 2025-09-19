import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../globals.dart';

class PetScreen extends StatefulWidget {
  const PetScreen({super.key});

  @override
  State<PetScreen> createState() => _PetScreenState();
}

class _PetScreenState extends State<PetScreen> {
  final nameController = TextEditingController();
  final weightController = TextEditingController();
  final colorController = TextEditingController();
  final ageController = TextEditingController();

  Future<void> createPet() async {
    FocusScope.of(context).unfocus(); // Fecha o teclado

    // Validação de campos vazios
    if (nameController.text.isEmpty ||
        weightController.text.isEmpty ||
        colorController.text.isEmpty ||
        ageController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Todos os campos são obrigatórios")),
      );
      return;
    }

    // Verifica se o usuário está autenticado
    if (jwtToken == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Usuário não autenticado")),
      );
      return;
    }

    try {
      final response = await http.post(
        Uri.parse("https://petadopt.onrender.com/pet/create"),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $jwtToken",
        },
        body: jsonEncode({
          "name": nameController.text,
          "weight": weightController.text,
          "color": colorController.text,
          "age": ageController.text,
        }),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Pet cadastrado com sucesso!")),
        );
        // Limpa os campos
        nameController.clear();
        weightController.clear();
        colorController.clear();
        ageController.clear();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Erro ao cadastrar pet: ${response.body}")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Erro de conexão: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Cadastro de Pet")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Column(
            children: [
              TextField(
                controller: nameController,
                decoration: const InputDecoration(labelText: "Nome"),
              ),
              TextField(
                controller: weightController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: "Peso"),
              ),
              TextField(
                controller: colorController,
                decoration: const InputDecoration(labelText: "Cor"),
              ),
              TextField(
                controller: ageController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: "Idade"),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: createPet,
                child: const Text("Cadastrar Pet"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
