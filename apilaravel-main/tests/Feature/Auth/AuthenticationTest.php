<?php

namespace Tests\Feature\Auth;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use Tymon\JWTAuth\Facades\JWTAuth;

class AuthenticationTest extends TestCase
{
    use RefreshDatabase;

    public function test_usuario_pode_logar_com_credenciais_corretas()
    {
        $user = User::factory()->create([
            'password' => bcrypt($password = 'i-love-laravel'),
        ]);

        $response = $this->postJson('/api/login', [
            'email' => $user->email,
            'password' => $password,
        ]);

        $response
            ->assertStatus(200)
            ->assertJsonStructure([
                'access_token',
                'token_type',
                'expires_in',
            ]);
    }

    public function test_usuario_nao_pode_logar_com_credenciais_incorretas()
    {
        $user = User::factory()->create([
            'password' => bcrypt('i-love-laravel'),
        ]);

        $response = $this->postJson('/api/login', [
            'email' => $user->email,
            'password' => 'wrong-password',
        ]);

        $response->assertStatus(401);
    }

    public function test_usuario_pode_acessar_rota_protegida_com_token_valido()
    {
        $user = User::factory()->create();
        $token = JWTAuth::fromUser($user);

        $response = $this->withHeader('Authorization', 'Bearer ' . $token)
                         ->postJson('/api/me');

        $response
            ->assertStatus(200)
            ->assertJson([
                'id' => $user->id,
                'email' => $user->email,
            ]);
    }

    public function test_usuario_nao_pode_acessar_rota_protegida_sem_token()
    {
        $response = $this->postJson('/api/me');

        $response->assertStatus(401);
    }

    public function test_usuario_pode_fazer_logout()
    {
        $user = User::factory()->create();
        $token = JWTAuth::fromUser($user);

        $response = $this->withHeader('Authorization', 'Bearer ' . $token)
                         ->postJson('/api/logout');

        $response
            ->assertStatus(200)
            ->assertJson([
                'message' => 'Successfully logged out',
            ]);

        // Verifica se o token foi invalidado
        $this->withHeader('Authorization', 'Bearer ' . $token)
             ->postJson('/api/me')
             ->assertStatus(401);
    }
}
