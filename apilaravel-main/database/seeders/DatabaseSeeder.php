<?php

namespace Database\Seeders;

// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Autor;
use App\Models\Categoria;
use App\Models\Livro;
use App\Models\Emprestimo;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // Cria um usuário admin
        User::factory()->create([
            'name' => 'Admin User',
            'email' => 'admin@example.com',
            'type' => 'admin',
        ]);

        // Cria 10 usuários estudantes
        User::factory(10)->create();

        // Cria 50 empréstimos
        Emprestimo::factory(50)->create();
    }
}
