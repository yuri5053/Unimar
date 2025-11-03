<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use App\Models\User;
use App\Models\Livro;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Emprestimo>
 */
class EmprestimoFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        return [
            'user_id' => User::factory(),
            'livro_id' => Livro::factory(),
            'data_emprestimo' => $this->faker->dateTimeBetween('-1 month', 'now'),
            'data_devolucao' => $this->faker->optional(0.5)->dateTimeBetween('now', '+1 month'),
        ];
    }
}
