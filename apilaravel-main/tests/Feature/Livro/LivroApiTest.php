<?php

namespace Tests\Feature\Livro;

use App\Models\Autor;
use App\Models\Categoria;
use App\Models\Livro;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use Tymon\JWTAuth\Facades\JWTAuth;

class LivroApiTest extends TestCase
{
    use RefreshDatabase;

    protected $user;
    protected $token;

    protected function setUp(): void
    {
        parent::setUp();
        $this->user = User::factory()->create();
        $this->token = JWTAuth::fromUser($this->user);
    }

    public function test_pode_listar_livros()
    {
        Livro::factory()->count(3)->create();

        $response = $this->withHeader('Authorization', 'Bearer ' . $this->token)
                         ->getJson('/api/livros');

        $response->assertStatus(200)
                 ->assertJsonCount(3, 'data');
    }

    public function test_pode_criar_um_livro()
    {
        $autor = Autor::factory()->create();
        $categoria = Categoria::factory()->create();

        $livroData = [
            'titulo' => 'Novo Livro de Teste',
            'autor_id' => $autor->id,
            'categoria_id' => $categoria->id,
            'ano_publicacao' => 2025,
        ];

        $response = $this->withHeader('Authorization', 'Bearer ' . $this->token)
                         ->postJson('/api/livros', $livroData);

        $response->assertStatus(201)
                 ->assertJsonFragment(['titulo' => 'Novo Livro de Teste']);

        $this->assertDatabaseHas('livros', ['titulo' => 'Novo Livro de Teste']);
    }

    public function test_pode_exibir_um_livro()
    {
        $livro = Livro::factory()->create();

        $response = $this->withHeader('Authorization', 'Bearer ' . $this->token)
                         ->getJson('/api/livros/' . $livro->id);

        $response->assertStatus(200)
                 ->assertJsonFragment(['id' => $livro->id]);
    }

    public function test_pode_atualizar_um_livro()
    {
        $livro = Livro::factory()->create();
        $novoTitulo = 'Titulo do Livro Atualizado';

        $updateData = [
            'titulo' => $novoTitulo,
            'autor_id' => $livro->autor_id,
            'categoria_id' => $livro->categoria_id,
            'ano_publicacao' => $livro->ano_publicacao,
        ];

        $response = $this->withHeader('Authorization', 'Bearer ' . $this->token)
                         ->putJson('/api/livros/' . $livro->id, $updateData);

        $response->assertStatus(200)
                 ->assertJsonFragment(['titulo' => $novoTitulo]);

        $this->assertDatabaseHas('livros', ['id' => $livro->id, 'titulo' => $novoTitulo]);
    }

    public function test_pode_deletar_um_livro()
    {
        $livro = Livro::factory()->create();

        $response = $this->withHeader('Authorization', 'Bearer ' . $this->token)
                         ->deleteJson('/api/livros/' . $livro->id);

        $response->assertStatus(204);

        $this->assertDatabaseMissing('livros', ['id' => $livro->id]);
    }
}
