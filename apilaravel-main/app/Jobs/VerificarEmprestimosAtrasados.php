<?php

namespace App\Jobs;

use App\Models\Emprestimo;
use Carbon\Carbon;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;

class VerificarEmprestimosAtrasados implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        Log::info('Verificando empréstimos atrasados...');

        $limite = Carbon::now()->subDays(7);

        $emprestimosAtrasados = Emprestimo::whereNull('data_devolucao')
            ->where('data_emprestimo', '<=', $limite)
            ->get();

        foreach ($emprestimosAtrasados as $emprestimo) {
            Log::warning('Empréstimo atrasado: ID ' . $emprestimo->id . ' - Livro ID: ' . $emprestimo->livro_id);
            // Aqui você poderia adicionar lógica para notificar o usuário, por exemplo.
        }

        Log::info('Verificação de empréstimos atrasados concluída.');
    }
}
